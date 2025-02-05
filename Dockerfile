# FROM python:3.9
# WORKDIR /app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt
# COPY . .
# EXPOSE 6000
# CMD ["python", "./services/app.py"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 4000

# Define environment variable to run in development mode
ENV FLASK_APP=services/app.py
ENV FLASK_ENV=development

# Run Flask when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
