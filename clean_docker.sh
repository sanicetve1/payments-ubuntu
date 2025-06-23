#!/bin/bash

echo "🔍 Stopping running containers named 'payments-agent'..."
docker ps -a --filter "ancestor=payments-agent" --format "{{.ID}}" | xargs -r docker stop

echo "🗑️ Removing containers named 'payments-agent'..."
docker ps -a --filter "ancestor=payments-agent" --format "{{.ID}}" | xargs -r docker rm

echo "🗑️ Removing image 'payments-agent'..."
docker images "payments-agent" --format "{{.ID}}" | xargs -r docker rmi -f

echo "✅ Cleanup complete."

