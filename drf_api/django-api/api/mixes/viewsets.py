from api.mixes.serializers import MixSerializer
from api.mixes.models import Mix
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import mixins
from django.http import HttpResponse

import requests
import json

class MixesViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin
):
    queryset = Mix.objects.all()
    serializer_class = MixSerializer
    permission_classes = (IsAuthenticated,)

    error_message = {"success": False, "msg": "Error updating playlist"}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = Mix.objects.get(id=request.data.get("id"))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        id = request.data.get("id")

        if not id:
            raise ValidationError(self.error_message)

        if self.request.playlist.pk != int(id):
            raise ValidationError(self.error_message)

        self.update(request)

        return Response({"success": True}, status.HTTP_200_OK)