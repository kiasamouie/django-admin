from api.socials.serializers import SocialSerializer 
from api.socials.models import Social
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

class SocialViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = SocialSerializer
    permission_classes = (IsAuthenticated,)

    error_message = {"success": False, "msg": "Error updating social"}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = Social.objects.get(id=request.data.get("id"))
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

        if self.request.social.pk != int(id):
            raise ValidationError(self.error_message)

        self.update(request)
        return Response({"success": True}, status.HTTP_200_OK)
