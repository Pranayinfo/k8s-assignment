FROM python:3.9.7-slim-buster

ADD . .

WORKDIR /

RUN pip install -r requirements.txt

ENV ASPNETCORE_URLS=http://+:9000

ENV PORT 9000

EXPOSE 9000

ENTRYPOINT ["python3"]

CMD ["app.py"]
