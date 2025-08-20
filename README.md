# 🛒 Интернет-магазин API

REST API для интернет-магазина, разработанный на Django с использованием Django REST Framework.

## 🚀 Возможности

- **Пользователи**: Регистрация, авторизация, профиль, личный баланс
- **Товары**: Просмотр каталога товаров (только для чтения)
- **Корзина**: Добавление, удаление, изменение количества товаров
- **Заказы**: Создание заказов с проверкой остатков и баланса
- **Администрирование**: Управление товарами через Django Admin

## 🛠 Технологии

- **Python 3.11+**
- **Django 4+**
- **Django REST Framework**
- **PostgreSQL**
- **JWT авторизация**
- **Docker + Docker Compose**
- **drf-spectacular** для документации API

## 📋 Требования

- Docker
- Docker Compose

## 🚀 Быстрый запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/M1dian/Internet-shop_project
cd internet-shop_project
```

2. Запустите проект:
```bash
docker-compose up --build
```

3. Откройте в браузере:
- **API**: http://localhost:8000/api/
- **Документация API**: http://localhost:8000/api/schema/swagger-ui/
- **Админ панель**: http://localhost:8000/admin/

## 🔧 Настройка окружения

Создайте файл `.env` в корне проекта:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:postgres@db:5432/shop_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📚 API Документация

### Аутентификация

Все защищенные эндпоинты требуют JWT токен в заголовке:
```
Authorization: Bearer <your-jwt-token>
```

### Основные эндпоинты

#### Пользователи
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход
- `GET /api/auth/profile/` - Профиль пользователя
- `PATCH /api/auth/profile/` - Обновление профиля
- `POST /api/auth/balance/` - Пополнение баланса

#### Товары
- `GET /api/products/` - Список товаров
- `GET /api/products/{id}/` - Детали товара

#### Корзина
- `GET /api/cart/` - Просмотр корзины
- `POST /api/cart/add/` - Добавить товар в корзину
- `PATCH /api/cart/update/` - Изменить количество
- `DELETE /api/cart/remove/{id}/` - Удалить товар из корзины

#### Заказы
- `GET /api/orders/` - История заказов
- `POST /api/orders/create/` - Создать заказ из корзины
- `GET /api/orders/{id}/` - Детали заказа

## 🧪 Тестирование

Запуск тестов:
```bash
docker-compose exec web python manage.py test
```

## 📁 Основная структура проекта

```
internet-shop/
├── app/                    # Основные приложения
│   ├── users/              # Пользователи и аутентификация
│   ├── products/           # Товары и категории
│   ├── cart/               # Корзина покупок
│   ├── orders/             # Заказы и их обработка
│   ├── core/               # Общие компоненты
│   └── logs/               # Логи
├── config/                 # Настройки Django
├── tests/                  # Тесты
├── docker-compose.yml      # Docker Compose
├── Dockerfile              # Docker образ
├── requirements.txt        # Зависимости
├── README.md               # Основная документация
├── DEPLOYMENT.md           # Инструкции по развертыванию
├── PROJECT_SUMMARY.md      # Краткое описание проекта
├── DOCUMENTATION_INDEX.md  # Индекс документации проекта
└── *.sh                    # Скрипты управления
```

## 🔐 Администрирование

1. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

2. Откройте http://localhost:8000/admin/
3. Войдите с созданными учетными данными
4. Управляйте товарами, пользователями и заказами

## 📝 Логирование

Все заказы логируются в консоль и файл `logs/orders.log`

## 🐳 Docker команды

```bash
# Запуск
docker-compose up --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f web

# Выполнение команд в контейнере
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```