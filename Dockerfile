FROM python:3.9
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat
COPY . .
EXPOSE 4000
CMD ["python", "./services/app.py"]