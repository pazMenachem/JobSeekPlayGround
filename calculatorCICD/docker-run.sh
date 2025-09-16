#!/usr/bin/env bash
# Simple Docker script for calculatorCICD
set -e

IMAGE="calculatorcicd"
CONTAINER="calculatorcicd-container"

echo "🐳 Building Docker image..."
docker build -t "$IMAGE" .

echo "🚀 Running calculator in Docker..."
docker run --rm --name "$CONTAINER" "$IMAGE"

echo "✅ Done!"