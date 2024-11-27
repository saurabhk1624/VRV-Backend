FROM python:3.12-alpine
RUN apk add --no-cache \
    python3-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    mariadb-connector-c-dev \
    build-base \
    pkgconfig

RUN python3 -m pip install --no-cache-dir -U pip
WORKDIR /assignment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /assignment
COPY requirements.txt .
RUN pip install -r requirements.txt
