
FROM python:3.8.16-slim-buster

RUN apt update
RUN apt install -y redis 

WORKDIR /root
ADD python-device-stub/requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /data

ADD astarte-interfaces ./astarte-interfaces
ADD python-device-stub/src ./src

CMD ["python", "src/main.py"]