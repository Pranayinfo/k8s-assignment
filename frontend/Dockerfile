FROM python:3.9.7-slim-buster

ADD . ./app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3"]

CMD ["app.py"]