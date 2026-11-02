#!/bin/bash

cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found. Install Python 3 and try again."
    read -r -p "Press Return to close this window..."
    exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "Creating the app's Python environment..."
    if ! python3 -m venv .venv; then
        echo "Could not create a Python environment."
        read -r -p "Press Return to close this window..."
        exit 1
    fi
fi

if ! .venv/bin/python -c "import tkinter" >/dev/null 2>&1; then
    echo "Tkinter is missing from this Python installation."
    echo "Install Python 3 from https://www.python.org/downloads/macos/ and try again."
    read -r -p "Press Return to close this window..."
    exit 1
fi

if ! .venv/bin/python -c "import PIL" >/dev/null 2>&1; then
    echo "Installing Pillow for the desktop app..."
    if ! .venv/bin/python -m pip install "pillow>=10.0.0"; then
        echo "Could not install Pillow."
        read -r -p "Press Return to close this window..."
        exit 1
    fi
fi

.venv/bin/python steg_app.py
status=$?

if [ "$status" -ne 0 ]; then
    echo "The application could not start or exited with an error."
    read -r -p "Press Return to close this window..."
fi

exit "$status"
