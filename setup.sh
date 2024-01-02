#!/usr/bin/env bash
echo "Installing required packages for Feedsphere"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt-get update
  sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
fi

rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install falcon gunicorn httpie