FROM python:3.11.11-bullseye

RUN apt-get update && apt-get install -y iputils-ping && apt-get clean

WORKDIR /services

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


#if using password authentication for ssh then install sshpass 
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*


COPY . .

COPY certs /certs

CMD ["uvicorn", "services:app", "--host=0.0.0.0", "--port=8000", "--ssl-keyfile=/certs/key.pem", "--ssl-certfile=/certs/cert.pem", "--reload"]