
FROM python:3.8.16-slim-buster

ADD linux_stub/requirements.txt app/

WORKDIR /app

RUN apt update && \
    apt install -y virtualenv git

RUN pip install -r requirements.txt

ADD astarte-interfaces astarte-interfaces
ADD linux_stub/src/ .

CMD ["python", "main.py"]