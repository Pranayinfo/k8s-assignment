FROM python:3.9.4-slim-buster

ADD . .

WORKDIR /

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3"]

CMD ["app.py"]