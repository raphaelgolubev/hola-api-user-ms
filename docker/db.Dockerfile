FROM postgres:14.1-alpine AS base

# Определяем аргументы
ARG PG_USER
ARG PG_PWD
ARG PG_DB

 # Указываем переменные окружения, используя аргументы
ENV POSTGRES_USER=${PG_USER}
ENV POSTGRES_PASSWORD=${PG_PWD}
ENV POSTGRES_DB=${PG_DB}

# Копируем скрипты инициализации в контейнер
COPY ./docker-postgres-sql/initialize.sh /docker-entrypoint-initdb.d/

# Устанавливаем права на выполнение для скрипта инициализации
RUN chmod +x /docker-entrypoint-initdb.d/initialize.sh