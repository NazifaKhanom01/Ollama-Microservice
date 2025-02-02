from flask import Flask, request, jsonify
import ollama
from flask_cors import CORS

app = Flask(__name__)

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
        # Call Ollama Model (Mistral or Llama)
        local_response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        response_text = local_response['message']['content']
        print("DONE!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({
            "local_response": response_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
