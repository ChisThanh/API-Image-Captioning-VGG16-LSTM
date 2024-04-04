# Use a Python base image
FROM python:3.10.12

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask application
# CMD ["python3", "index.py"]


# docker build -t flask-app .
# docker run -p 5000:5000 flask-app
