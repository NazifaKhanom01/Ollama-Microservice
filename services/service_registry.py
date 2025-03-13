# from flask import Flask, request, jsonify
# import etcd3
# import requests

# app = Flask(__name__)

# # Connect to etcd
# etcd = etcd3.client(host='localhost', port=2379)

# # Base path in etcd where services will be registered
# SERVICES_PATH = "services/"

# @app.route('/register', methods=['POST'])
# def register_service():
#     """ Register a service with etcd """
#     data = request.json
#     service_name = data.get("name")
#     service_address = data.get("address")

#     if not service_name or not service_address:
#         return jsonify({"error": "Missing service name or address"}), 400

#     # Register service in etcd
#     etcd.put(f"{SERVICES_PATH}{service_name}", service_address)

#     return jsonify({"message": f"Service {service_name} registered successfully"}), 200

# @app.route('/services', methods=['GET'])
# def list_services():
#     """ List all registered services from etcd """
#     services = {}
#     for key, value in etcd.get_prefix(SERVICES_PATH):
#         services[key.decode().replace(SERVICES_PATH, '')] = value.decode()

#     return jsonify(services)

# @app.route('/forward', methods=['POST'])
# def forward_message():
#     """ Forward message to another service """
#     data = request.json
#     target_service = data.get("to")
#     message = data.get("message")

#     if not target_service or not message:
#         return jsonify({"error": "Missing target service or message"}), 400

#     # Find the target service address from etcd
#     target_address = etcd.get(f"{SERVICES_PATH}{target_service}")[0]

#     if target_address:
#         target_url = f"http://{target_address.decode()}/receive"
#         response = requests.post(target_url, json={"message": message})
#         return response.json(), response.status_code
#     else:
#         return jsonify({"error": "Service not found"}), 404

# @app.route('/receive', methods=['POST'])
# def receive_message():
#     """ Receive a forwarded message """
#     data = request.json
#     message = data.get("message")
#     return jsonify({"message": f"Received message: {message}"}), 200

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)



import logging
from flask import Flask, request, jsonify
import etcd3
import time
import threading

import requests

app = Flask(__name__)
etcd = etcd3.client(host='localhost', port=2379)  # Connect to etcd

SERVICE_TTL = 150  # Time to live for service entries (2.5 minutes)
HEARTBEAT_INTERVAL = 120  # Services must send a heartbeat every 2 minutes


def register_service_in_etcd(service_name, service_url):
    lease = etcd.lease(SERVICE_TTL)  # Create a lease for auto-expiry
    etcd.put(f"/services/{service_name}", service_url, lease=lease)
    etcd.put(f"/heartbeats/{service_name}", str(time.time()), lease=lease)

# 1. Service Registration
@app.route('/register', methods=['POST'])
def register_service():
    data = request.json
    service_name = data.get("service_name")
    service_url = data.get("service_url")

    if not service_name or not service_url:
        return jsonify({"error": "Missing service_name or service_url"}), 400

    try:
        register_service_in_etcd(service_name, service_url)
        return jsonify({"message": "Service registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Retrieve Available Services
@app.route('/service-list', methods=['GET'])
def get_services():
    services = {}
    for value, metadata in etcd.get_all():
         key = metadata.key.decode("utf-8")
         if key.startswith("/services/"):
            service_name = key.split("/services/")[-1]
            services[service_name] = value.decode("utf-8")

    return jsonify(services), 200

# 3. Message Forwarding
@app.route('/message', methods=['POST'])
def forward_message():
    data = request.json
    target_service = data.get("target_service")
    payload = data.get("payload")

    if not target_service or not payload:
        return jsonify({"error": "Target service and payload are required"}), 400

    service_url, _ = etcd.get(f"/services/{target_service}")

    if service_url is None:
        return jsonify({"error": "Service not found"}), 404

    service_url = service_url.decode("utf-8")
    try:
        response = requests.post(service_url, json=payload)
        return jsonify({"message": "Message forwarded successfully", "response": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to reach {target_service}: {str(e)}"}), 500

# 4. Heartbeat Mechanism
@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    service_name = data.get("service_name")

    if not service_name:
        return jsonify({"error": "Service name is required"}), 400

    if etcd.get(f"/services/{service_name}")[0] is None:
        return jsonify({"error": "Service not registered"}), 404

    lease = etcd.lease(SERVICE_TTL)  # Renew lease
    etcd.put(f"/services/{service_name}", etcd.get(f"/services/{service_name}")[0], lease=lease)
    etcd.put(f"/heartbeats/{service_name}", str(time.time()), lease=lease)
    return jsonify({"message": "Heartbeat received!"}), 200

# 5. Get All Registered Services from Etcd
@app.route('/check-services', methods=['GET'])
def check_services():
    try:
        services = {}
        
        # Query Etcd for all services under /services/
        for value, metadata in etcd.get_all():
            key = metadata.key.decode("utf-8")
            if key.startswith("/services/"):
                service_name = key.split("/services/")[-1]
                services[service_name] = value.decode("utf-8")

        if not services:
            return jsonify({"message": "No services found in Etcd"}), 404

        return jsonify({"services": services}), 200

    except Exception as e:
        logging.error(f"Error fetching services: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
 # 5. Cleanup expired services
def cleanup_services():
    while True:
        time.sleep(60)
        for value, metadata in etcd.get_all():
            key = metadata.key.decode("utf-8")
            if key.startswith("/heartbeats/"):
                service_name = key.split("/heartbeats/")[-1]
                last_heartbeat, _ = etcd.get(f"/heartbeats/{service_name}")
                if last_heartbeat is None or (time.time() - float(last_heartbeat.decode("utf-8")) > SERVICE_TTL):
                    etcd.delete(f"/services/{service_name}")
                    etcd.delete(f"/heartbeats/{service_name}")
                    logging.info(f"Service {service_name} removed due to inactivity")

cleanup_thread = threading.Thread(target=cleanup_services, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
