
FROM python:3.8.16-slim-buster

ADD linux-stub/requirements.txt app/

WORKDIR /app

RUN apt update && \
    apt install -y virtualenv git

RUN pip install -r requirements.txt

ADD linux-stub/scene-settings.json ./
ADD astarte-interfaces astarte-interfaces
ADD linux-stub/src/ .

CMD ["python", "main.py"]