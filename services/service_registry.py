from flask import Flask, request, jsonify
import etcd3
import requests

app = Flask(__name__)

# Connect to etcd
etcd = etcd3.client(host='localhost', port=2379)

# Base path in etcd where services will be registered
SERVICES_PATH = "services/"

@app.route('/register', methods=['POST'])
def register_service():
    """ Register a service with etcd """
    data = request.json
    service_name = data.get("name")
    service_address = data.get("address")

    if not service_name or not service_address:
        return jsonify({"error": "Missing service name or address"}), 400

    # Register service in etcd
    etcd.put(f"{SERVICES_PATH}{service_name}", service_address)

    return jsonify({"message": f"Service {service_name} registered successfully"}), 200

@app.route('/services', methods=['GET'])
def list_services():
    """ List all registered services from etcd """
    services = {}
    for key, value in etcd.get_prefix(SERVICES_PATH):
        services[key.decode().replace(SERVICES_PATH, '')] = value.decode()

    return jsonify(services)

@app.route('/forward', methods=['POST'])
def forward_message():
    """ Forward message to another service """
    data = request.json
    target_service = data.get("to")
    message = data.get("message")

    if not target_service or not message:
        return jsonify({"error": "Missing target service or message"}), 400

    # Find the target service address from etcd
    target_address = etcd.get(f"{SERVICES_PATH}{target_service}")[0]

    if target_address:
        target_url = f"http://{target_address.decode()}/receive"
        response = requests.post(target_url, json={"message": message})
        return response.json(), response.status_code
    else:
        return jsonify({"error": "Service not found"}), 404

@app.route('/receive', methods=['POST'])
def receive_message():
    """ Receive a forwarded message """
    data = request.json
    message = data.get("message")
    return jsonify({"message": f"Received message: {message}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
