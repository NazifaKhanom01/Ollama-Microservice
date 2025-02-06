from flask import Flask, request,render_template, jsonify
import ollama
import requests
import json  
from flask_cors import CORS

app = Flask(__name__)

OLLAMA_HOST =  "http://ollama:11434"

CORS(app)

@app.route('/generate', methods=['POST'])
def generate_response():
    print("Starting ............")
    """Handles requests and forwards to Ollama (local LLM)."""
    data = request.json

    prompt = data.get("prompt", "")

    model = data.get("model", "mistral")  

    if not prompt:
        return render_template('index.html', response="Prompt is required.")

        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={"model": model, "messages": [{"role": "user", "content": prompt}]},
            stream=True
        )
        print("Raw Ollama Response:", response.text) 

        if response.status_code == 200:

            response_text = ""
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        json_chunk = json.loads(chunk.decode("utf-8"))
                        if json_chunk.get("done"):
                            print("DONE!!!!!!!!!!!!!!!!!!!!!!")
                            break  
                        response_text += json_chunk.get("message", {}).get("content", "")
                    except json.JSONDecodeError:
                        continue  


            return jsonify({"local_response": response_text})
            
        else:
            return jsonify({"error": "Ollama API error", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
