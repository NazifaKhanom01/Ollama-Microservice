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

    # Ensure sender service info is included
    sender_service = payload.get("sender_service", "unknown_sender")
    payload["sender"] = sender_service

    try:
        response = requests.post(service_url, json=payload)
        response_data = response.json()
        # Add the responding service name to the response
        response_data["response_from"] = target_service
        response_data["received_from"] = sender_service

        # return jsonify({"message": "Message forwarded successfully", "response": response.json()})
        return jsonify({"message": "Message forwarded successfully", "response": response_data})

    
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
