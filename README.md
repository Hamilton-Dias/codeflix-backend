# Codeflix backend

Application written in python 3 for Full Cycle 3.0 course.

To run the program:
<pre>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
docker run -d --hostname rabbitmq --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
docker run -p 8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.2.4 start-dev
python manage.py startconsumer
python manage.py runserver
</pre>

## What this project is
This is the final project for the Full Cycle 3.0 course. This repository contains the backend code for a video streaming service, the codeflix.
It is a sample project that allows users to upload videos. We need the codeflix-frontend to work with this project as the final user.
The admin users will need the codeflix-admin to manage the videos. Technologies used:
- DDD
- Clean archtecture
- Python 3
- Python venv
- Django
- RabbitMQ
- Events Driven Archtecture
- Unit and Integration tests
- E2E Tests
- Keycloak
- Docker
- Docker Compose
- Mysql
- Elasticsearch
- Kafka
- Kafka connect
- GraphQL
