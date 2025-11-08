#!/bin/bash

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    ./bin/setup.sh
fi

venv/bin/python src/main.py