FROM python:3.11-slim

WORKDIR /mcp-servers

COPY ./mcp_servers/requirements.txt /mcp-servers/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /mcp-servers/requirements.txt

COPY ./mcp_servers/app /mcp-servers/app
COPY ./mcp_servers/spec /mcp-servers/spec