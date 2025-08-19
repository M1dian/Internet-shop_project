#!/bin/bash

echo "📊 Статус интернет-магазина..."
echo ""

# Проверяем статус контейнеров
echo "🐳 Статус контейнеров:"
docker-compose ps

echo ""

# Проверяем логи
echo "📝 Последние логи веб-приложения:"
docker-compose logs --tail=10 web

echo ""

# Проверяем доступность API
echo "🌐 Проверка доступности API..."
if curl -s http://localhost:8000/api/ > /dev/null; then
    echo "✅ API доступен по адресу: http://localhost:8000/api/"
else
    echo "❌ API недоступен"
fi

echo ""

# Показываем полезные команды
echo "💡 Полезные команды:"
echo "   🚀 Запуск: ./start_project.sh"
echo "   🛑 Остановка: ./stop_project.sh"
echo "   📊 Логи: docker-compose logs -f web"
echo "   🧪 Тесты: docker-compose exec web python manage.py test"
echo "   🗄️  База данных: docker-compose exec db psql -U postgres -d shop_db" 