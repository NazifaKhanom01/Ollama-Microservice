FROM python:3.9
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["python", "./services/app.py"]

# FROM ollama/ollama:latest AS ollama

# FROM python:3.9
# WORKDIR /app
# COPY . /app
# RUN pip install --no-cache-dir -r requirements.txt
# COPY --from=ollama /usr/bin/ollama /usr/bin/ollama

# ENV FLASK_APP=services/app.py
# ENV FLASK_ENV=development

# EXPOSE 4000
# CMD ["bash", "-c", "\
#   ollama serve & \
#   sleep 5 && \
#   ollama pull mistral && \
#   flask --app services/app.py run --host=0.0.0.0 --port=4000"]