#!/usr/bin/env bash
echo "Installing required packages for feedsphere"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt-get update
  sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
else
  echo "Please install better OS (e.g. Linux) :)"
  exit
fi

rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install falcon gunicorn httpie cerbeus beatifulsoup4 feedparser alembic sqlalchemy bcrypt apscheduler