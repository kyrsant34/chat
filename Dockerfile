FROM python:3.6-alpine3.7

# Install dependencies
RUN apk add build-base libffi-dev mariadb-dev

# Install dependencies
RUN apk add bash mariadb-client-libs

COPY . /code/

WORKDIR /code

RUN pip install -r requirements.txt
