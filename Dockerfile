FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN apk update
RUN apk add bash

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

RUN apk del .build-deps

COPY . .

ENV PYTHONPATH=/app:/app/backend
ENV DJANGO_SETTINGS_MODULE=backend.core.settings

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.core.wsgi:application"]