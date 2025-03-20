# from flask import Flask, request,render_template, jsonify
# import ollama
# import requests
# import json  
# from flask_cors import CORS

# app = Flask(__name__)

# OLLAMA_HOST =  "http://ollama:11434"

# CORS(app)

# @app.route('/generate', methods=['POST'])
# def generate_response():
#     print("Starting ............")
#     """Handles requests and forwards to Ollama (local LLM)."""
#     data = request.json

#     prompt = data.get("prompt", "")

#     model = data.get("model", "mistral")  

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400
    
#     try:
#         response = requests.post(
#             f"{OLLAMA_HOST}/api/chat",
#             json={"model": model, "messages": [{"role": "user", "content": prompt}]},
#             stream=True
#         )
#         print("Raw Ollama Response:", response.text) 

#         if response.status_code == 200:

#             response_text = ""
#             for chunk in response.iter_lines():
#                 if chunk:
#                     try:
#                         json_chunk = json.loads(chunk.decode("utf-8"))
#                         if json_chunk.get("done"):
#                             print("DONE!!!!!!!!!!!!!!!!!!!!!!")
#                             break  
#                         response_text += json_chunk.get("message", {}).get("content", "")
#                     except json.JSONDecodeError:
#                         continue  


#             return jsonify({"local_response": response_text})
            
#         else:
#             return jsonify({"error": "Ollama API error", "details": response.text}), response.status_code

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=4000, debug=True)




from flask import Flask, request, jsonify
import requests
import json  
import threading
import time

app = Flask(__name__)

OLLAMA_HOST = "http://localhost:11434"
SERVICE_NAME = "revathi-llm-service"
SERVICE_URL = "http://10.190.10.160:4000/generate"
SERVICE_REGISTRY = "http://10.190.10.160:5002"

# Register Service on Startup
def register_service():
    data = {"service_name": SERVICE_NAME, "service_url": SERVICE_URL}
    requests.post(f"{SERVICE_REGISTRY}/register", json=data)

# Heartbeat Mechanism
def send_heartbeat():
    while True:
        time.sleep(120)
        try:
            response = requests.post(f"{SERVICE_REGISTRY}/heartbeat", json={"service_name": SERVICE_NAME})
            if response.status_code != 200:
                print("Re-registering service...")
                register_service()
        except requests.exceptions.RequestException:
            print("Service registry unavailable!")

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    prompt = data.get("prompt", "")
    sender = data.get("sender", "unknown_sender")  # Identify sender
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
                "received_from": sender
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
    print("payload from llm", payload)
    if not target_service or not payload:
        return jsonify({"error": "Target service and payload are required"}), 400
    # Include sender service name in the payload
    payload["sender"] = SERVICE_NAME
    
    # Send a message to the Service Registry
    response = requests.post(f"{SERVICE_REGISTRY}/message", json={"target_service": target_service, "payload": payload})
    return jsonify(response.json())

# Start Registration and Heartbeat in Threads
threading.Thread(target=register_service, daemon=True).start()
threading.Thread(target=send_heartbeat, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)

