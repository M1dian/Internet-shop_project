# 🚀 Инструкция по развертыванию

## 📋 Предварительные требования

- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)
- **Git** (для клонирования репозитория)

## 🔧 Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd internet-shop
```

### 2. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и настройте переменные:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:postgres@db:5432/shop_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Запуск проекта

#### Автоматический запуск (рекомендуется)

```bash
./start_project.sh
```

Этот скрипт автоматически:
- Проверит наличие Docker
- Остановит существующие контейнеры
- Соберет и запустит проект
- Выполнит миграции
- Создаст суперпользователя
- Инициализирует тестовые данные

#### Ручной запуск

```bash
# Сборка и запуск
docker-compose up --build -d

# Ожидание готовности базы данных
sleep 10

# Миграции
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python create_superuser.py

# Инициализация тестовых данных
docker-compose exec web python manage.py init_data
```

## 🌐 Доступ к приложению

После успешного запуска:

- **API**: http://localhost:8000/api/
- **Документация API**: http://localhost:8000/api/schema/swagger-ui/
- **Админ панель**: http://localhost:8000/admin/

## 👤 Тестовые пользователи

- **Администратор**:
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@shop.com`

- **Тестовый пользователь**:
  - Username: `testuser`
  - Password: `testpass123`
  - Email: `test@example.com`

## 🛠 Управление проектом

### Проверка статуса

```bash
./status_project.sh
```

### Остановка проекта

```bash
./stop_project.sh
```

### Просмотр логов

```bash
# Все логи
docker-compose logs

# Логи веб-приложения
docker-compose logs -f web

# Логи базы данных
docker-compose logs -f db
```

### Выполнение команд в контейнере

```bash
# Django shell
docker-compose exec web python manage.py shell

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic

# Очистка кэша
docker-compose exec web python manage.py clearcache
```

## 🧪 Тестирование

### Запуск всех тестов

```bash
docker-compose exec web python manage.py test
```

### Запуск тестов конкретного приложения

```bash
docker-compose exec web python manage.py test app.users
docker-compose exec web python manage.py test app.products
docker-compose exec web python manage.py test app.cart
docker-compose exec web python manage.py test app.orders
```

### Запуск тестов с покрытием

```bash
docker-compose exec web python manage.py test --with-coverage
```

## 🗄️ База данных

### Подключение к PostgreSQL

```bash
docker-compose exec db psql -U postgres -d shop_db
```

### Резервное копирование

```bash
docker-compose exec db pg_dump -U postgres shop_db > backup.sql
```

### Восстановление из резервной копии

```bash
docker-compose exec -T db psql -U postgres shop_db < backup.sql
```

## 🔍 Отладка

### Проверка контейнеров

```bash
# Статус контейнеров
docker-compose ps

# Детальная информация о контейнере
docker-compose exec web python manage.py check

# Проверка настроек
docker-compose exec web python manage.py diffsettings
```

### Перезапуск сервисов

```bash
# Перезапуск веб-приложения
docker-compose restart web

# Перезапуск базы данных
docker-compose restart db

# Перезапуск всех сервисов
docker-compose restart
```

## 🚨 Устранение неполадок

### Проблемы с базой данных

```bash
# Проверка подключения
docker-compose exec web python manage.py dbshell

# Сброс базы данных
docker-compose down -v
docker-compose up --build -d
```

### Проблемы с миграциями

```bash
# Откат миграций
docker-compose exec web python manage.py migrate --fake-initial

# Сброс миграций
docker-compose exec web python manage.py migrate --fake app_name zero
```

### Проблемы с правами доступа

```bash
# Проверка прав на файлы
ls -la

# Исправление прав
chmod +x *.sh
chmod 755 app/
```

## 📊 Мониторинг

### Проверка ресурсов

```bash
# Использование ресурсов контейнерами
docker stats

# Проверка дискового пространства
docker system df
```

### Очистка неиспользуемых ресурсов

```bash
# Удаление неиспользуемых образов
docker image prune

# Удаление неиспользуемых контейнеров
docker container prune

# Полная очистка
docker system prune -a
```

## 🔄 Обновление проекта

```bash
# Остановка проекта
./stop_project.sh

# Получение обновлений
git pull origin main

# Пересборка и запуск
./start_project.sh
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f web`
2. Убедитесь, что все сервисы запущены: `docker-compose ps`
3. Проверьте настройки в файле `.env`
4. Убедитесь, что порты 8000 и 5432 свободны

## 📚 Дополнительные ресурсы

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) 