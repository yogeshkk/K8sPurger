FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apk add curl

COPY . .

CMD [ "python3", "K8sPurger.py","--type=svc" ]
