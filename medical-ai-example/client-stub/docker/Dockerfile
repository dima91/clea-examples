
FROM python:3.8.16-slim-buster

ADD client-stub/requirements.txt app/

WORKDIR /app

RUN pip install -r requirements.txt

ADD astarte-interfaces astarte-interfaces
ADD client-stub/src/ .

CMD ["python", "main.py"]