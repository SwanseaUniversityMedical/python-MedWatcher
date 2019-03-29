FROM python:rc-alpine

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./watch.py" ]
