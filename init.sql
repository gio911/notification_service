-- Создаём базу данных auth_db (если скрипт выполняется вручную, удали эту строку)
CREATE DATABASE auth_db;

-- Предоставляем привилегии на базу данных auth_db пользователю postgres
GRANT ALL PRIVILEGES ON DATABASE auth_db TO postgres;

-- Переключаемся на базу auth_db
\c auth_db;

-- Создаём таблицу users в схеме public (по умолчанию)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY, 
    login VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50)
);

-- Вставка данных с фиксированным UUID для id
INSERT INTO users (id, login, first_name, last_name, email)
VALUES ('123e4567-e89b-12d3-a456-426614174000', 'test_user', 'John', 'Doe', 'john.doe@example.com')
ON CONFLICT (login) DO NOTHING;
