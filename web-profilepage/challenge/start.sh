#!/bin/sh

echo "Starting server..."
until npm start; do
    echo "Server 'index.js' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done