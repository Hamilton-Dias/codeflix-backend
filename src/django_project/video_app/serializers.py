from rest_framework import serializers
from src.core.video.domain.value_objets import Rating

class VideoRatingField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    year_launched = serializers.IntegerField()
    opened = serializers.BooleanField(default=False)
    rating = VideoRatingField(required=True)
    duration = serializers.IntegerField()
    categories_id = SetField(child=serializers.UUIDField(), required=False)
    genres_id = SetField(child=serializers.UUIDField(), required=False)
    cast_members_id = SetField(child=serializers.UUIDField(), required=False)

class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
