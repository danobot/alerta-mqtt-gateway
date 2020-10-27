docker stop alerta-mqtt
docker rm alerta-mqtt
docker build -t danobot/alerta-mqtt .
docker run -d --restart=unless-stopped -e MQTT_HOST="tower.local" -e ALERTA_ENDPOINT="http://web:8763" -e ALERTA_API_KEY="a7RtkQqM5PngVpmGnW4vb4hzBVZfBX3RZ6oMZiB8N9XUvJhuCNveNvbC5XvLhPF" -v $(pwd):/app --name alerta-mqtt danobot/alerta-mqtt
docker logs alerta-mqtt
