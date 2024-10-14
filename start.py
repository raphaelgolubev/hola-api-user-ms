"""
    Это краткая история о том, как я чуть не получил нервный срыв
    
    Начнем с того, что у меня было запущено два окна Visual Studio Code, в одном окне папка hola-api-register-ms,
    в другом hola-api-user-ms.
    
    Я ШЕСТЬ ЧАСОВ (!!!!) потратил на изучение бага, который не позволял мне поднять
    сервисы в docker-compose.yaml для user-ms и для register-ms.
    Проблема заключалась в том, что вместо переменных окружения для user-ms, 
    подставлялись переменные окружения для register-ms.
    Я переименовал .env файлы в обоих папках, чтобы они имели уникальное имя:
    - .user-ms.env в папке hola-api-user-ms
    - .register-ms.env в папке hola-api-register-ms
    
    Команда `docker-compose config` показывала, что в одной части файла docker-compose.yaml
    подставляются правильные данные, а в другой части - неправильные.
    Поэтому я решил написать скрипт, который будет подставлять переменные окружения в docker-compose.yaml вручную.
    Ниже представлен скрипт, который это делает. Я выполнил его и заметил, что подставились значения
    из файла .register-ms.env, хотя прописан путь до .user-ms.env. Это просто сводило меня с ума.

    Я удалял все контейнеры, образы и тома. Затем все пересобирал. Ничего не помогало.
    Прошерстив весь интернет и не найдя ответа, я додумался перезапустить IDE. 
    Это решило проблему.
    
    Я оставлю этот код здесь как напоминание, что порой полезно просто перезапустить IDE.
    Видимо, данные были закэшированны самим VS Code или что или как, я вообще хуй знает.
"""

# import os
# from dotenv import load_dotenv  # pip install python-dotenv
# import yaml  # pip install pyyaml


# # Загружаем переменные окружения из .env файла
# load_dotenv(dotenv_path='.user-ms.env')


# # Функция для удаления комментариев
# def remove_comments(value):
#     return value.split('#')[0].strip()


# # Получаем все параметры с префиксом POSTGRES_ и удаляем комментарии
# postgres_env_variables = {
#     key: remove_comments(os.getenv(key))
#     for key in os.environ.keys() if key.startswith('POSTGRES_')
# }


# with open('docker-compose.yaml', 'r') as file:
#     docker_compose = yaml.safe_load(file)


# # Добавление переменных окружения в секцию postgres
# docker_compose['services']['postgres-user-ms']['environment'] = postgres_env_variables
# docker_compose['services']['postgres-user-ms']['ports'] = [f'{postgres_env_variables['POSTGRES_PORT']}:{postgres_env_variables['POSTGRES_PORT']}']


# # Сохранение обновленного docker-compose.yaml
# with open('docker-compose.yaml', 'w') as file:
#     yaml.dump(docker_compose, file)

# for key, value in postgres_env_variables.items():
#     print(f'{key} = {value}')
