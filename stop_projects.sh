#!/bin/bash

echo "🛑 Остановка интернет-магазина..."
echo ""

# Останавливаем контейнеры
docker-compose down

echo "✅ Проект остановлен"
echo ""

# Показываем статус
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "💡 Для запуска проекта используйте: ./start_project.sh" 