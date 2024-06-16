# Pull Python image from Dockerhub
FROM python:3.10-slim 

# Directory of container
WORKDIR /app

# Copy current directory into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose app on port 80 for local view
EXPOSE 80

# Run application
ENV FLASK_APP=src
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]