FROM python:3.9.7-slim-buster

ADD . .

WORKDIR /

ENV ASPNETCORE_URLS=http://+:9000

ENV PORT 9000

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["python3"]

CMD ["app.py"]
