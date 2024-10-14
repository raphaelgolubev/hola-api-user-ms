# Проверяем, существует ли файл .env
# if [ ! -f .env ]; then
#     echo ".env файл не найден!"
#     exit 1
# fi

# Читаем файл .env построчно
while IFS= read -r line; do
    # Удаляем комментарии и кавычки
    clean_line=$(echo "$line" | sed 's/#.*//; s/"//g; s/'\''//g')

    # Удаляем пробелы перед и после знака '='
    clean_line=$(echo "$clean_line" | sed 's/ *= */=/g')

    # Если строка не пустая, экспортируем переменную
    if [ -n "$clean_line" ]; then
        echo "exporting variable:" $clean_line 
        export $clean_line
    fi
done < .env

psql -v --username $POSTGRES_USER --dbname $POSTGRES_DB <<-EOSQL
    CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
    CREATE DATABASE $POSTGRES_DB WITH OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL
