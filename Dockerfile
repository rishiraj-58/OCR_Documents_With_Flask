FROM python:3.8-slim-buster

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

# Set the working directory and copy the requirements file
WORKDIR /app
COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt && pip3 install tensorflow

# Change the ownership of the application directory to the non-root user
RUN chown -R appuser /app

# Switch to the non-root user
USER appuser

# Expose the port
EXPOSE 8090

# Run the application
CMD ["python", "server.py"]

