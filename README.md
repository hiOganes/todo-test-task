# todo-test-task API

## Table of Contents

- [Description](#description)
- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Endpoints](#endpoints)
- [Testing](#testing)

## Description:
 
### Это простое Todo-приложение на Django REST Framework с задачами (tasks). Пользователь может управлять своими задачами: создавать, просматривать список, менять статус (pending ↔ completed) и удалять.
#### После аутентификации пользователь попадает на страничку, где он может управлять своими задачами

#### Было создано 3 приложения:
###### - accounts (модель с данными о пользователе) модель от AbstractUser так как в ней уже есть все необходимые поля дял пользователя. Также пполе логин был изменен на email
###### - common (это абстрактная модель для реализиции общей логики в целя соблюдения принципа DRY)
###### - tasks (модель с данными о задачах юзера, с отрношением "многие к одному" c моделью accounts)
#### Была создана папка "core" в которой находятся настройки и будущие конфигурации проекта
#### 100% бэкэнда покрыто тестами
#### Документация вынесена в отдельный файл "schema_examples.py"
#### Generic Views (минимум кода, встроенная обработка стандартных операций, легко читаемо)
#### backend и frontend разделены по отдельным директориям (для читаемости и развития независимо друг от друга)
## Technologies

- Python 3.12.3
- Django 6.0

## Installation and start project

1. Clone the repository
    ```
    git@github.com:hiOganes/todo-test-task.git
    ```

2. In the terminal, at the docker-compose.yaml file level, run the command:
    ```
    docker compose up --build
    ```

3. Next, you need to connect to the project. Open new terminal and using the command:
    ```
    docker compose exec web bash
    ```
### inside the container / bash

1. Apply migrations:
    ```
    python backend/manage.py migrate
    ```

2. Create a superuser:
    ```
    python backend/manage.py createsuperuser
    ```

## Endpoints

1. Open [website](http://127.0.0.1:8001/)
1. Open your browser and go to [OpenAPI](http://127.0.0.1:8001/api/schema/swagger-ui/)

## Testing

### inside the container / bash
 ```
 python backend/manage.py test .
 ```

## Table of Contents

- [Description](#description)
- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Endpoints](#endpoints)
- [Testing](#testing)