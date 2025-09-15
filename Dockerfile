FROM python:3.11-slim

WORKDIR /mcp-fin

COPY ./requirements.txt /mcp-fin/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /mcp-fin/requirements.txt

COPY ./app /mcp-fin/app