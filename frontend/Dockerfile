FROM python:3.9.7-slim-buster

ADD . ./app

WORKDIR /app

#ENV ASPNETCORE_URLS=http://+:8000

#ENV PORT 8000

RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["python3"]

CMD ["app.py"]
