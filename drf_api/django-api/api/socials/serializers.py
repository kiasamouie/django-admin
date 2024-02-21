from rest_framework import serializers
from .models import Social

class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Social 
        fields = "__all__"
        read_only_field = ["id"]
