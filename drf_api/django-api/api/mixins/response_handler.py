from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib import messages

class ResponseHandlerMixin:
    def handle_response(self, request, success_message=None, error_message=None, warning_message=None, status=200):
        if request.path.startswith('/api/'):
            # API request, return JSON response
            if success_message:
                return Response({'message': success_message}, status=status)
            elif error_message:
                return Response({'message': error_message}, status=status)
            elif warning_message:
                return Response({'message': warning_message}, status=status)
        else:
            # Admin request, use messages framework
            if success_message:
                messages.success(request, success_message)
            elif error_message:
                messages.error(request, error_message)
            elif warning_message:
                messages.warning(request, warning_message)
            return redirect('admin:api_playlists_playlist_changelist')
