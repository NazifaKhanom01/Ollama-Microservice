# Flask + Ollama Local Model Integration

This project provides a **Flask API** that interacts with **Ollama**'s local language models such as **Mistral** and **Gemma3**. It allows users to send requests and ask questions to the models via a POST request to the `/generate` endpoint.

## **Prerequisites**

Before running this project, ensure that you have the following installed on your system:

- **Docker and Docker Compose**  
  [Download Docker](https://www.docker.com)
  
- **Python 3.10+**  
  [Download Python](https://www.python.org/downloads/)
  
- **Ollama**  
  [Download Ollama](https://ollama.com/download) and install it on your system.

- **Mistral Model**  
  Once Ollama is installed, you can download the **Mistral** model by running the following command:
  ```bash
  ollama pull mistral
  ```

- **Gemma3 Model**  
  Similarly, you can download the **Gemma3** model by running:
  ```bash
  ollama pull gemma3
  ```

---

## **Setup & Installation**

### **For Running with Docker**

1. **Clone the Repository**

   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/NazifaKhanom01/Ollama-Microservice
   cd Ollama-Microservice
   ```

2. **Build and Start the Containers**

   After navigating to the project directory, run the following command to build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

   This command will pull the necessary images, set up the environment, and download the required models. This process may take some time.

---

### **For Running Directly on Your OS**

1. **Clone the Repository**

   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/NazifaKhanom01/Ollama-Microservice
   cd Ollama-Microservice
   ```

2. **Install Ollama**

   Download and install Ollama from [Ollama's official website](https://ollama.com/download).

   After installation, download the **Mistral** model by running:
   ```bash
   ollama pull mistral
   ```

3. **Create a Virtual Environment**

   It's a good practice to use a virtual environment to manage Python dependencies. Create a virtual environment by running:
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**

   Activate the virtual environment:

   - **Windows (PowerShell)**:
     ```bash
     .\venv\Scripts\Activate
     ```
   
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**

   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Flask Application**

   To start the Flask app locally, run the following command:
   ```bash
   python app.py
   ```

   The Flask app will now be running at `http://localhost:4000`.

---

## **Usage and Testing the Service**

You can interact with the Flask API by sending a **POST request** to the `/generate` endpoint.

### **Request Example**

Send a POST request with the following JSON body:
```json
{
  "prompt": "Can you tell me about different types of colours?",
  "model": "mistral"
}
```

You can test the endpoint using **cURL**:
```bash
curl -X POST http://localhost:4000/generate -H "Content-Type: application/json" -d '{"prompt": "Can you tell me about different types of colours?", "model": "mistral"}'
```

### **Response Example**

The response will look something like this:
```json
{
  "local_response": "There are many types of colours, including primary colours like red, blue, and yellow..."
}
```

---

## **Creating a Docker Container for the Microservice**

To create a Docker container for the microservice, create a `Dockerfile` in the root directory with the following contents:

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["python", "./services/app.py"]
```

### **Build and Run the Docker Image**

1. **Build the Docker Image**:
   ```bash
   docker build -t ollamaservice .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d -p 4000:4000 ollamaservice
   ```

This will start the Flask application inside a Docker container, exposing the service on port 4000.

---

## Additional step
## created a simple static webpage to show the LLM's response using angular
## repository link for the webpage
https://github.com/revathisekar19/llm-app.git