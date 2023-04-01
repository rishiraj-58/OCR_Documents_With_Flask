FROM python:3.8-slim-buster

# Install system packages
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy the requirements file to the container and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && pip3 install tensorflow

# Copy the source code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]

