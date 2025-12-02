#!/bin/bash

echo "Starting multiple traffic tests..."

# Ping test
ping -c 20 google.com >/dev/null &

# HTTP request
curl -s https://example.com >/dev/null &

# File download test
wget -O /dev/null http://speedtest.tele2.net/1MB.zip >/dev/null &

echo "All traffic tests started."
