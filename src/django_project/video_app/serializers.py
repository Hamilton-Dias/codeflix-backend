from rest_framework import serializers

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    rating = serializers.CharField()
    duration = serializers.IntegerField()
    opened = serializers.BooleanField()
    published = serializers.BooleanField(required=False)
    categories = SetField(child=serializers.UUIDField(), required=False)
    genres = SetField(child=serializers.UUIDField(), required=False)
    cast_members = SetField(child=serializers.UUIDField(), required=False)

class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
