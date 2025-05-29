#!/bin/bash

COMMIT_HASH=$(git rev-parse --short HEAD)

MODEL_NAME="latest-${COMMIT_HASH}.tar.gz"
MODEL_PATH="models/${MODEL_NAME}"

echo "🚀 Training model..."
poetry run rasa train --domain domain --out models/

LATEST_TRAINED=$(ls -t models/*.tar.gz | head -n1)

if [ -f "$LATEST_TRAINED" ]; then
    mv "$LATEST_TRAINED" "$MODEL_PATH"
    echo "✅ Model saved as $MODEL_PATH"
else
    echo "❌ No model found to rename."
fi
