FROM python:3.12-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости для компиляции (если нужны, например, для psycopg2 или pillow)
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# Копируем requirements и устанавливаем Python-пакеты
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Удаляем build-зависимости (чтобы образ был легче)
RUN apk del .build-deps

# Копируем весь проект
COPY . .

# САМОЕ ВАЖНОЕ: добавляем /app в PYTHONPATH
ENV PYTHONPATH=/app/backend
ENV DJANGO_SETTINGS_MODULE=backend.core.settings

# Опционально: миграции при старте (можно раскомментировать)
# RUN python backend/manage.py migrate --noinput

EXPOSE 8000

# Правильный запуск Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "backend.core.wsgi:application"]