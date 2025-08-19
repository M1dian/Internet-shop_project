FROM python:3.11-slim

# Установка системных зависимостей для подготовки контейнера к работе с Python и Django
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей проекта
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY . .

# Создание директорий для логов
RUN mkdir -p /logs  # Создаём общую директорию для логов (можно использовать для volume, если нужно)
RUN mkdir -p /app/logs  # Создаём директорию /app/logs для файлов логов Django

# Создание директорий для логов
RUN mkdir -p /logs

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Открытие порта для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.8000"]
