
FROM python:3.8.16-slim-buster

ADD python-stub/requirements.txt app/

WORKDIR /app

# RUN apt update && \
#     apt install -y virtualenv git

RUN pip install -r requirements.txt

ADD astarte-interfaces astarte-interfaces
ADD python-stub/config.json ./
ADD python-stub/src/ .

CMD ["python", "main.py"]