# FROM gcr.io/distroless/python3-debian11
FROM python:3.10.9-slim-bullseye

COPY . /app

WORKDIR /app

RUN pip install --upgrade -r requirements.txt

ENV HOST=0.0.0.0
ENV PORT=8765
ENV SSL_KEYFILE=
ENV SSL_CERTFILE=

EXPOSE $PORT

CMD ["python", "src/main.py"]
