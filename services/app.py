from flask import Flask, request, jsonify
import ollama
import requests
import json  
from flask_cors import CORS

app = Flask(__name__)

OLLAMA_HOST = "http://host.docker.internal:11434"

# Enable CORS to allow external access
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_response():
    print("Starting ............")
    """Handles requests and forwards to Ollama (local LLM)."""
    data = request.json

    prompt = data.get("prompt", "")

    model = data.get("model", "mistral")  # Default to mistral if no model is specified

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        # Call Ollama API running on the host machine
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={"model": model, "messages": [{"role": "user", "content": prompt}]},
            stream=True
        )
        print("Raw Ollama Response:", response.text) 

        if response.status_code == 200:

            # response_data = response.json()
            # response_text = response_data.get("message", {}).get("content", "")
            # print("DONE!!!!!!!!!!!!!!!!!!!!!!")
            response_text = ""
            # Iterate over the streamed response chunks
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode("utf-8"))
                        if json_chunk.get("done"):
                            print("DONE!!!!!!!!!!!!!!!!!!!!!!")
                            break  # Stop when 'done' is true
                        response_text += json_chunk.get("message", {}).get("content", "")
                    except json.JSONDecodeError:
                        continue  # Ignore malformed chunks


            return jsonify({"local_response": response_text})
            
        else:
            return jsonify({"error": "Ollama API error", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
