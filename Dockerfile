FROM python:3.7-slim-buster

# RUN apt-get update && apt-get install -y python3-dev build-essential

# Definition of the API URL endpoint
# ENV API_URL = https://group6-container.internal.ashysea-af4b5413.westeurope.azurecontainerapps.io

RUN mkdir -p /projet/
WORKDIR /projet/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# CMD ["python", "main.py"]
CMD ["bash", "-c", "uvicorn main:api_router --host 0.0.0.0 --port 80"]




# FROM python:3.7-slim-buster
# # FROM python:3.8-buster

# RUN mkdir -p /projet/files
# WORKDIR /projet/files

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 80

# CMD ["python", "files/api.py"]
# # CMD ["uvicorn", "files.api:app", "--host", "0.0.0.0", "--port", "80"]