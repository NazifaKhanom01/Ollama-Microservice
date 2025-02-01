# from flask import Flask, request, jsonify
# import ollama
# import requests
# from flask_cors import CORS

# app = Flask(__name__)

# # Enable CORS to allow external access
# CORS(app)

# # Define external LLM endpoints (e.g., OpenAI, Claude, etc.)
# EXTERNAL_LLM_URLS = {
#     "openai": "https://api.openai.com/v1/chat/completions",
#     "custom_llm": "http://another-ip:5000/generate"  # Replace with actual external LLM microservice
# }


# @app.route('/generate', methods=['POST'])
# def generate_response():
#     """Handles requests and forwards to local or external LLMs."""
#     data = request.json
#     prompt = data.get("prompt", "")
#     model = data.get("model", "mistral")  # Default to mistral

#     if not prompt:
#         return jsonify({"error": "Prompt is required"}), 400

#     try:
#         # Call Local LLM (Ollama)
#         local_response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
#         response_text = local_response['message']['content']
        
#         # Call External LLMs (Example: OpenAI API)
#         external_responses = {}
#         for name, url in EXTERNAL_LLM_URLS.items():
#             try:
#                 if name == "openai":
#                     external_responses[name] = requests.post(
#                         url,
#                         headers={"Authorization": f"Bearer <Your_OpenAI_API_Key>"},
#                         json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
#                     ).json().get("choices", [{}])[0].get("message", {}).get("content", "")
#                 else:
#                     external_responses[name] = requests.post(url, json={"prompt": prompt}).json().get("response", "")
#             except Exception as e:
#                 external_responses[name] = f"Error: {str(e)}"

#         return jsonify({
#             "local_response": response_text,
#             "external_responses": external_responses
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


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
