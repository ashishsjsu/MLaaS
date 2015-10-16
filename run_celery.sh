#!/usr/bin/env bash

source venv/bin/activate
celery worker -A flaskapp.celery --loglevel=info --concurrency=1
