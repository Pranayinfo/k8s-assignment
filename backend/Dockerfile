FROM python:3.9.7-slim-buster

ADD . .

WORKDIR /

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["python3"]

CMD ["app.py"]
