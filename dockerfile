FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

CMD ["python", "src/main.py"]
