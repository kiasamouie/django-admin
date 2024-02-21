from rest_framework import serializers
from api.playlists.serializers import PlaylistSerializer
from .models import Mix

class MixSerializer(serializers.ModelSerializer):
    playlist = PlaylistSerializer()

    class Meta:
        model = Mix 
        fields = [field.name for field in Mix._meta.get_fields()] + ['playlist']
        read_only_field = ["id"]
