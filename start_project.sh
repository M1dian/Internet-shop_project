#!/bin/bash

echo "🚀 Запуск интернет-магазина..."
echo ""

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"
echo ""

# Останавливаем существующие контейнеры
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Собираем и запускаем проект
echo "🔨 Сборка и запуск проекта..."
docker-compose up --build -d

# Ждем готовности базы данных
echo "⏳ Ожидание готовности базы данных..."
sleep 10

# Выполняем миграции
echo "🗄️  Выполнение миграций..."
docker-compose exec -T web python manage.py migrate

# Создаем суперпользователя
echo "👑 Создание суперпользователя..."
docker-compose exec -T web python create_superuser.py

# Инициализируем тестовые данные
echo "📦 Инициализация тестовых данных..."
docker-compose exec -T web python manage.py init_data

echo ""
echo "🎉 Проект успешно запущен!"
echo ""
echo "📱 Доступные URL:"
echo "   🌐 API: http://localhost:8000/api/"
echo "   📚 Документация API: http://localhost:8000/api/schema/swagger-ui/"
echo "   🔐 Админ панель: http://localhost:8000/admin/"
echo ""
echo "👤 Тестовые пользователи:"
echo "   👑 Админ: admin / admin123"
echo "   👤 Пользователь: testuser / testpass123"
echo ""
echo "📋 Полезные команды:"
echo "   🛑 Остановка: docker-compose down"
echo "   📊 Логи: docker-compose logs -f web"
echo "   🧪 Тесты: docker-compose exec web python manage.py test"
echo "" 