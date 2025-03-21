# Flask + Ollama Local Model Integration(Service Discovery Implementation)

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

# For Ollama + Microservice Assignment:

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

## **Additional Step: Static Webpage Integration**

For a simple static webpage that displays the LLM's response, we have integrated an Angular frontend. You can find the repository for this webpage at the following link:

[LLM App Webpage Repository](https://github.com/revathisekar19/llm-app.git)

---

## **Directory Structure**

The directory structure of the project is as follows:

```
Ollama-Microservice/
│
├── docker-compose.yml         # Docker Compose configuration file
├── Dockerfile                 # Dockerfile to build the Flask microservice container
├── requirements.txt           # Python dependencies
├── app.py                     # Main Flask app
├── services/                  # Service-related files (Flask routes, etc.)
└── README.md                  # Project documentation
```

---

## **Conclusion**

This project provides a basic integration between Flask and the Ollama API, allowing you to interact with language models like **Mistral** and **Gemma3** via a RESTful API. You can run the service locally using Python or via Docker, and you can test it using cURL or any API client.








