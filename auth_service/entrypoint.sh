#!/bin/bash
set -e  # Прекращает выполнение при любой ошибке
set -x  # Показывает все команды, которые выполняются

# Ожидаем доступности PostgreSQL
# echo "POSTGRES_HOST=$POSTGRES_HOST"
# echo "SQL_PORT=$SQL_PORT"

# until pg_isready -h "$POSTGRES_HOST" -p "$SQL_PORT"; do
#   echo "Ожидание PostgreSQL ($POSTGRES_HOST:$SQL_PORT)..."
#   sleep 1
# done
# alembic stamp head
# alembic revision --autogenerate -m "Initial migration"

# # Применение миграций
# echo "Применяем миграции Alembic..."
# if alembic upgrade head; then
#     echo "Миграции успешно применены."
# else
#     echo "Ошибка при применении миграций Alembic!"
#     exit 1
# fi

# Создание суперпользователя
# echo "Создание ролей и прав..."
# python ./src/init_scripts/superuser_creation.py
# echo "Роли и права созданы."

# Запуск FastAPI
echo "Запускаем FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload





























# # Очистка папки с миграциями
# echo "Удаляем старые миграции..."
# if [ -d "./migrations/versions" ]; then
#   rm -rf ./migrations/versions/*
#   echo "Файлы миграций удалены."
# else
#   echo "Папка ./migrations/versions не существует, пропускаем удаление."
# fi


# echo "Удаляем все данные из базы данных..."
# export PGPASSWORD="$POSTGRES_PASSWORD"
# psql -h "$POSTGRES_HOST" -p "$SQL_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB_AUTH" -v ON_ERROR_STOP=1 -c "
# DO \$\$
# DECLARE
#     truncate_query TEXT;
# BEGIN
#     SELECT INTO truncate_query
#         'TRUNCATE TABLE ' || string_agg(quote_ident(schemaname) || '.' || quote_ident(tablename), ', ') || ' CASCADE'
#     FROM pg_tables
#     WHERE tableowner = current_user
#       AND schemaname NOT IN ('pg_catalog', 'information_schema')
#       AND tablename NOT LIKE 'pg_%';

#     IF truncate_query IS NOT NULL THEN
#         EXECUTE truncate_query;
#     END IF;
# END \$\$;
# "
# echo "Данные из базы данных удалены..."

# Создание миграции (только в режиме разработки)
# if [ "$ENVIRONMENT" == "development" ]; then
#   echo "Создаем миграцию..."
#   alembic revision --autogenerate -m "Initial migration"
#   echo "Миграция создана."
# fi

