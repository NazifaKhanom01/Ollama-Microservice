# Use a multi-stage build where stage 1 copies the Ollama binary
FROM ollama/ollama:latest AS ollama

FROM python:3.9-slim
WORKDIR /app

# Copy your application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Ollama binary from the first stage
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama

# Set environment variables for Flask
ENV FLASK_APP=services/app.py
ENV FLASK_ENV=development

# Expose the Flask port
EXPOSE 4000

# Start Ollama, wait, pull the model, then start Flask
CMD ["bash", "-c", "\
  ollama serve & \
  sleep 5 && \
  ollama pull mistral && \
  flask --app services/app.py run --host=0.0.0.0 --port=4000"]
