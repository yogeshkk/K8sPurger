FROM python:3.8-alpine3.12

WORKDIR /app

RUN apk add --no-cache curl
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

CMD [ "python3", "-u", "K8sPurger.py","--type=svc" ]
