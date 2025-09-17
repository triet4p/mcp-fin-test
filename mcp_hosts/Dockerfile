FROM python:3.11-slim

WORKDIR /mcp-hosts

COPY ./mcp_hosts/requirements.txt /mcp-hosts/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /mcp-hosts/requirements.txt

COPY ./mcp_hosts /mcp-hosts/

RUN chmod +x /mcp-hosts/entrypoint.sh