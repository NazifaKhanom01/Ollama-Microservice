from flask import Flask, request, jsonify
import requests
import json  
import threading
import time

app = Flask(__name__)

OLLAMA_HOST = "http://localhost:11434"
SERVICE_NAME = "nazifa-llm-service"
SERVICE_URL = "http://10.160.18.167:4001/generate"
SERVICE_REGISTRY = "http://10.190.10.160:5002"

# Register Service on Startup
def register_service():
    data = {"service_name": SERVICE_NAME, "service_url": SERVICE_URL}
    requests.post(f"{SERVICE_REGISTRY}/register", json=data)

# Heartbeat Mechanism (Every 2 Minutes)
def send_heartbeat():
    while True:
        time.sleep(120)
        requests.post(f"{SERVICE_REGISTRY}/heartbeat", json={"service_name": SERVICE_NAME})

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    prompt = data.get("prompt", "")
    model = data.get("model", "mistral") 

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400


    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={"model": model, "messages": [{"role": "user", "content": prompt}]},
            stream=True
        )

        if response.status_code == 200:
            response_text = ""
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode("utf-8"))
                        if json_chunk.get("done"):

                            break  
                        response_text += json_chunk.get("message", {}).get("content", "")
                    except json.JSONDecodeError:
                        continue  

            # return jsonify({"local_response": response_text})
            return jsonify({
                "message": response_text,
                "response_from": SERVICE_NAME,  # Ensure response contains service name
            })

        else:
            return jsonify({"error": "Ollama API error", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch List of Services
@app.route('/service-list', methods=['GET'])
def list_services():
    response = requests.get(f"{SERVICE_REGISTRY}/service-list")
    return jsonify(response.json())

# Communicate with Friend's Microservice
@app.route('/message-friend', methods=['POST'])
def message_friend():
    data = request.json
    target_service = data.get("target_service")  
    payload = data.get("payload")

    if not target_service or not payload:
        return jsonify({"error": "Target service and payload are required"}), 400
    
    
    # Send a message to the Service Registry
    response = requests.post(f"{SERVICE_REGISTRY}/message", json={"target_service": target_service, "payload": payload})
    return jsonify(response.json())

# Start Registration and Heartbeat in Threads
threading.Thread(target=register_service, daemon=True).start()
threading.Thread(target=send_heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)
