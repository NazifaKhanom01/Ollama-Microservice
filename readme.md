# Flask + Ollama Local Model Integration

This project provides a simple Flask API that interacts with the **Ollama** local LLM (Mistral). It allows users to send requests and ask questions to the Mistral model via a POST request to the `/generate` endpoint. 

## **Prerequisites**
Before running the code, make sure you have the following:
- **Python 3.10+** → [Download here](https://www.python.org/downloads/)
- **Ollama** → [Download here](https://ollama.com/download) and install it on your system.
- **Mistral Model** → Once Ollama is installed, download the **Mistral** model via Ollama.

---

## **Setup & Installation**

### **1. Clone the Repository**
First, clone the repository to your local machine:
```bash
git clone https://github.com/NazifaKhanom01/Ollama-Microservice
cd Ollama-Microservice
```

### **2. Install Ollama**
Download and install Ollama from Ollama's official website. https://ollama.com/download

Once installed, make sure you have downloaded the Mistral model by running:
```bash
ollama run mistral
```

### **3. Create a Virtual Environment**
Create a Python virtual environment to manage dependencies:
```bash
python -m venv venv
```

### **4. Activate the Virtual Environment**
Activate the virtual environment:

Windows (PowerShell):
```bash
.\venv\Scripts\Activate
```
Mac/Linux:
```bash
source venv/bin/activate
```
## **5. Install Dependencies**
Install the required Python packages:

```bash
pip install -r requirements.txt
```

## **6. Run the Flask Application**
To start the Flask app locally, run:

```bash
python app.py
```

The Flask app will run on http://localhost:5000.

## Usage
Send a POST request to /generate endpoint with the following JSON body:
```json
{
  "prompt": "Can you tell me about different types of colours?",
  "model": "mistral"
}
```
Sample Request using cURL:
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Can you tell me about different types of colours?", "model": "mistral"}'
```
Response:
```json
{
  "local_response": "There are many types of colours, including primary colours like red, blue, and yellow..."
}
```

## Running it in docker container

To create an image run the following command.

 ```bash
 docker build -t ollama-local .
 ```

 Then to run the image locally run the following command
 
 ```bash
 docker run -p 4000:4000 -v ollama_models:/root/.ollama/models ollama-local
 ```

 The docker container will run with port 4000 exposed and then user can use the URL
 http://localhost:4000/generate to send post request in the follwoing format
 ```json
{
  "prompt": "Can you tell me about different types of colours?",
  "model": "mistral"
}
```
Sample Request using cURL:
```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Can you tell me about different types of colours?", "model": "mistral"}'
```
Response:
```json
{
  "local_response": "There are many types of colours, including primary colours like red, blue, and yellow..."
}
```