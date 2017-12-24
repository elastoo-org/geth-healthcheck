FROM python:2

WORKDIR /usr/src/app
COPY ethereum-hc.py .
EXPOSE 8082
CMD [ "python", "./ethereum-hc.py" ]