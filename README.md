# Codeflix backend

Application written in python 3 for Full Cycle 3.0 course.
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
