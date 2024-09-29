FROM python:3.11.7-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt