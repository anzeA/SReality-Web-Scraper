# Use the official Python image as the base image
FROM python:3.9

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY server.py .
CMD ["python", "server.py"]
