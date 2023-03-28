![example workflow](https://github.com/IgorKrupko-94/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# FOODGRAM-PROJECT-REACT
Логин: igor
Пароль: Wenger15@

## О чём проект:

Cайт Foodgram, «Продуктовый помощник». 
На этом сервисе пользователи смогут публиковать рецепты, 
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

## Главная страница
Содержимое главной страницы — список первых шести рецептов, 
отсортированных по дате публикации (от новых к старым).
Остальные рецепты доступны на следующих страницах: 
внизу страницы есть пагинация.

## Страница рецепта
На странице — полное описание рецепта. 
Для авторизованных пользователей — возможность добавить рецепт в избранное и в 
список покупок, возможность подписаться на автора рецепта.

## Страница пользователя
На странице — имя пользователя, все рецепты, опубликованные пользователем 
и возможность подписаться на пользователя.

## Подписка на авторов
Подписка на публикации доступна только авторизованному пользователю. 
Страница подписок доступна только владельцу.
# Сценарий поведения пользователя:
- Пользователь переходит на страницу другого пользователя или на страницу рецепта
и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
- Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, 
опубликованных теми авторами, на которых он подписался. 
- Сортировка записей — по дате публикации (от новых к старым).
- При необходимости пользователь может отказаться от подписки на автора: 
переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

## Список избранного
Работа со списком избранного доступна только авторизованному пользователю. 
Список избранного может просматривать только его владелец.
# Сценарий поведения пользователя:
- Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
- Пользователь переходит на страницу «Список избранного» и 
просматривает персональный список избранных рецептов.
- При необходимости пользователь может удалить рецепт из избранного.

## Список покупок
Работа со списком покупок доступна авторизованным пользователям. 
Список покупок может просматривать только его владелец.
# Сценарий поведения пользователя:
- Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
- Пользователь переходит на страницу Список покупок, 
там доступны все добавленные в список рецепты. 
- Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем 
и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
- При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt.


### Запуск проекта через docker-compose на удалённом сервере

Клонируйте репозиторий и перейдите в него в командной строке:
``` 
git clone git@github.com:IgorKrupko-94/foodgram-project-react.git
```
``` 
cd foodgram-project-react
```

Установите на сервере Docker, Docker Compose:
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

Скопируйте на сервер файлы docker-compose.yml, 
nginx.conf из папки infra (команды выполнять находясь в папке infra):
```
scp docker-compose.yml nginx.conf <username>@<IP>:/home/<username>/   # username - имя пользователя на сервере
                                                                      # IP - публичный IP сервера
```

Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```

Создать и запустить контейнеры Docker (выполните команды на сервере)
```
sudo docker-compose up -d
```

После успешной сборки выполнить миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```

Создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```

Соберите статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```


### Команды для заполнения базы ингредиентами:
* Копируем файл "ingredients.json" с фикстурами на сервер: 
(копирование нужно делать из папки /backend/foodgram/data/)
```
scp ingredients.json <username>@<ID>:/home/<username>/          # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```

* Копируем файл "ingredients.json" с фикстурами в контейнер:
  (копирование нужно делать на сервере)
```
sudo docker cp ingredients.json <CONTAINER ID>:/app          # CONTAINER ID - ID нужного контейнера, отвечающего за backend
```

* Применяем фикстуры:
```
sudo docker-compose exec backend python manage.py loaddata fixtures.json
```

После каждого обновления репозитория (push в ветку master) будет происходить:
* Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
* Сборка и доставка докер-образов frontend и backend на Docker Hub
* Разворачивание проекта на удаленном сервере
* Отправка сообщения в Telegram в случае успеха


# Author
## Igor Krupko
