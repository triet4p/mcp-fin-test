@echo off
echo Rebuilding all Docker images...

docker-compose down
docker build -t yf-service:1.0 -f yf/Dockerfile .
docker build -t mcp-fin-servers:1.0 -f mcp_servers/Dockerfile .
docker build -t mcp-fin-hosts:1.0 -f mcp_hosts/Dockerfile .

docker system prune -f
echo All images rebuilt successfully!