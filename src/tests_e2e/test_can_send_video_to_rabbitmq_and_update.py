import pytest
import json
import pika
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from src.core.video.infra.video_converted_rabbitmq_consumer import VideoConvertedRabbitMQConsumer
from src.django_project.jwt_auth_test_mixin import JWTAuthTestMixin
from src.django_project.video_app.models import Video as VideoORM

from rest_framework.status import (
  HTTP_201_CREATED
)

@pytest.mark.django_db
class TestCanSendVideoToRabbitMQAndUpdate(JWTAuthTestMixin):
  def test_can_send_video_to_rabbitmq_and_update(self) -> None:
    self.client = APIClient()
    self.authenticate_admin()
    
    # Cria categoria
    create_response = self.client.post(
      '/api/categories/', 
      data={
        "name": "Category 1",
        "description": "Category 1 description"
      }
    )
    assert create_response.status_code == HTTP_201_CREATED
    created_category_id = create_response.data['id']

    # Cria gênero
    genre_response = self.client.post(
      '/api/genres/', 
      data={
        "name": "Genre 1",
        "is_active": True,
        "categories": [created_category_id]
      }
    )
    assert genre_response.status_code == HTTP_201_CREATED
    created_genre_id = genre_response.data['id']

    # Cria cast member
    cast_member_response = self.client.post(
      '/api/cast_members/',
      data={
        "name": "Cast member 1",
        "type": "ACTOR"
      }
    )

    assert cast_member_response.status_code == HTTP_201_CREATED
    created_cast_member_id = cast_member_response.data['id']

    # Cria video
    video_response = self.client.post(
      '/api/videos/',
      data={
        "title": "Sample Video",
        "description": "Test description",
        "launch_year": 2023,
        "duration": 120,
        "rating": "L",
        "opened": False,
        "categories": [created_category_id],
        "genres": [created_genre_id],
        "cast_members": [created_cast_member_id]
      }
    )

    assert video_response.status_code == HTTP_201_CREATED
    video_id = video_response.data['id']

    assert VideoORM.objects.get(id=video_id) is not None

    # Cria um mock de arquivo 
    video_content = b"fake video content"
    video_file = SimpleUploadedFile(
        "test_video.mp4",
        video_content,
        content_type="video/mp4"
    )
    
    # Faz upload de media pro video
    video_update_response = self.client.patch(
      f'/api/videos/{video_id}/',
      data={"video_file": video_file},
      format="multipart"
    )

    assert video_update_response.status_code == HTTP_201_CREATED

    # Deixar o rabbitMQ rodando com o 
    # docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    # ou docker start rabbitmq caso ja tenha sido criado o container
    # e depois rodar o consumer: python manage.py startconsumer
    
    QUEUE = "videos.converted"
    HOST = "localhost"
    PORT = 5672

    connection = pika.BlockingConnection(
      pika.ConnectionParameters(
        host=HOST,
        port=PORT,
      ),
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)

    message = {
        "error": "",
        "video": {
            "resource_id": f"{video_id}.VIDEO",
            "encoded_video_folder": "/path/to/encoded/video",
        },
        "status": "COMPLETED",
    }
    channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

    consumer = VideoConvertedRabbitMQConsumer()
    is_consumed = consumer.consumeOne(channel)

    assert is_consumed is True

    connection.close()

    video_processed = VideoORM.objects.get(id=video_id)
    assert video_processed is not None
    assert video_processed.video.status == "COMPLETED"
