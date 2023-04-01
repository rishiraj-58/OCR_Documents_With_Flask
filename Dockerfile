FROM python:3.8

RUN apt-get update && \
    apt-get install -y cmake && \
    pip3 install -r requirements.txt
CMD ["python", "server.py"]
