#!/bin/bash
set -e  # Прекращает выполнение при любой ошибке
set -x  # Показывает все команды, которые выполняются

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

