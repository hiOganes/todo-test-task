# todo-test-task API

## Table of Contents

- [Decisions](#decisions)
- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Endpoints](#endpoints)
- [Testing](#testing)

## Decisions:


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

3. Next, you need to connect to the project terminal using the command:
    ```
    docker compose exec web bash
    ```
### inside the container / bash

1. Apply migrations:
    ```
    python manage.py migrate
    ```

2. Create a superuser:
    ```
    python manage.py createsuperuser
    ```

## Endpoints

1. Open your browser and go to [OpenAPI](http://127.0.0.1:8001/api/schema/swagger-ui/)

## Testing

### inside the container / bash
 ```
 python manage.py test .
 ```
#### or
### at the docker-compose.yaml file level, run the command:
 ```
 docker compose exec web python manage.py test .
 ```

## Table of Contents

- [Decisions](#decisions)
- [Technologies](#technologies)
- [Installation and start project](#installation-and-start-project)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Screenshots](#screenshots)