# Flask + Ollama Local Model Integration

This project provides a **Flask API** that interacts with **Ollama**'s local language models such as **Mistral** and **Gemma3**. It allows users to send requests and ask questions to the models via a POST request to the `/generate` endpoint.

## **Prerequisites**

Before running this project, ensure that you have the following installed on your system:

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

### **For Running Directly on Your OS**

### Etcd setup

1. **Pull the etcd Docker Image**
   
         docker pull quay.io/coreos/etcd:v3.5.0
   
3. **Run etcd as a Docker Container**
   
   docker run -d --name etcd `
  -p 2379:2379 -p 2380:2380 `
  -e ALLOW_NONE_AUTHENTICATION=yes `
  -e ETCD_ADVERTISE_CLIENT_URLS=http://0.0.0.0:2379 `
  quay.io/coreos/etcd:v3.5.0

5. **Verify the etcd Container is Running**

      docker ps
   
### **Code setup** 


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

### **System Architecture**

The main components involved are:

1. Service Registry: A Flask-based microservice that stores service information in Etcd
and provides endpoints for microservices to register, list services, send heartbeats, and
forward messages.
2. Microservices: Each microservice registers with the service registry at startup, retrieves
available services, sends messages via the registry, and periodically sends heartbeats.
3. Etcd Storage: Acts as the backend database for storing service information

## API Endpoints:
## Service Registry Endpoints
1. Service Registration:
        Endpoint: POST /register
        Function: Registers a microservice with the service registry.
2. Retrieve Available Services:
        Endpoint: GET /service-list
        Function: Returns a list of currently registered microservices.
3. Message Forwarding:
        Endpoint: POST /message
        Function: Forwards a message from one microservice to another.
4. Heartbeat Mechanism:
        Endpoint: POST /heartbeat
        Function: Updates the last-seen timestamp for a microservice, ensuring it remains in the service registry.
5. Query Etcd:
        Endpoint: POST /check-services
        Function: Query Etcd for all the services stored in it

## Microservice Endpoints
1. Response Generation:
        Endpoint: POST /generate
        Function: Generate the response to the microservice
2. Fetch list of Services:
        Endpoint: GET /service-list
        Function: Get the list of microservices from the service registry
3. Communication with Friend's Service:
        Endpoint: POST /message-friend
        Function: Send message to friend's service through the /message endpoint in the service registry


## **Usage and Testing the Service**

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






## Additional step
## created a simple static webpage to show the LLM's response using angular
## repository link for the webpage
https://github.com/revathisekar19/llm-app.git
