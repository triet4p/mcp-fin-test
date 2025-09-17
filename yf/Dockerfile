FROM python:3.11-slim

WORKDIR /yf

COPY ./yf/requirements.txt /yf/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /yf/requirements.txt

COPY ./yf/app /yf/app