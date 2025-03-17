FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

run apt update -y && apt install awscli -y
RUN apt-get update && pip insatall -r requirements.txt
CMD ["python3" , "app.py"]
