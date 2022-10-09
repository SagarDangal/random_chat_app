#!/bin/bash -e

echo "starting docker build"
docker build -f Dockerfile -t witit-chat-server:latest .

echo "starting container build"
docker container rm -f chat-api || true
docker image prune -f
docker run -d -p 127.0.0.1:8000:8080 --network=backend --name chat-api witit-chat-server

echo "container build finished"