
FROM python:3.8.16-slim-buster

ADD linux_stub/src/ app/
ADD astarte-interfaces app/

WORKDIR /app

RUN apt update && \
    apt install -y virtualenv git

RUN pip install -r requirements.txt

CMD ["python", "main.py"]