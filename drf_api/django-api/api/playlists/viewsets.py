from api.playlists.serializers import PlaylistSerializer
from api.playlists.models import Playlist
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.decorators import action
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache

import requests

class PlaylistViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin
):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated,)
    
    error_message = {"success": False, "msg": "Error updating playlist"}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = Playlist.objects.get(id=request.data.get("id"))
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
    
    @action(detail=False, methods=['post'])
    def fetch_urls(self, request):
        if request.path.startswith('/api/'):
            soundcloud_user_id = request.data.get('soundcloud_user_id')
        else:
            soundcloud_user_id = request.POST.get('soundcloud_user_id')

        response = False
        if not soundcloud_user_id:
            return self.handle_response(request,response,'soundcloud_user_id parameter is empty or missing',status.HTTP_400_BAD_REQUEST)
        
        playlists = self.request_soundcloud_playlists(soundcloud_user_id)
        if not len(playlists):
            return self.handle_response(request,response,"No new Playlists",status.HTTP_200_OK)
        
        playlists.reverse()
        response = len(playlists) == len(Playlist.objects.bulk_create(playlists))
        message = 'Playlists not Added'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if response:
            message = 'Playlists Added'
            status_code = status.HTTP_200_OK
        return self.handle_response(request,response,message,status_code)
        
    def request_soundcloud_playlists(self, soundcloud_user_id):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,de;q=0.7,fa;q=0.6',
            'Authorization': 'OAuth 2-293729-66593390-IqsLWFiWRwv0w3J',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://soundcloud.com',
            'Referer': 'https://soundcloud.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'client_id': 'WnapqLyoN0eHT0qfAtQSkZFrFkCgf8Gp',
            'limit': '10',
            'offset': '0',
            'linked_partitioning': '1',
            'app_version': '1681813797',
            'app_locale': 'en',
        }
        permalinks = Playlist.objects.all().values_list('permalink_url', flat=True)
        cache.clear()
        all_playlists = []
        def recursive_fetch(url):
            nonlocal all_playlists
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # Merge results under 'collection' key
                if 'collection' in data:
                    playlists = []
                    for i, p in enumerate(data['collection']):
                        try:
                            playlist = p['playlist']
                            if playlist['permalink_url'] in permalinks:
                                continue
                            # user     = p['user']
                            playlists.append(Playlist(
                                title=playlist['title'],
                                permalink_url=playlist['permalink_url'],
                                artwork_url=playlist['artwork_url'],
                                sc_playlist_id=playlist['id'],
                                duration=playlist['duration'],
                                track_count=playlist['track_count'],
                            ))
                        except:
                            continue
                    all_playlists.extend(playlists)
                if 'next_href' in data and data['next_href']:
                    recursive_fetch(data['next_href'])

        recursive_fetch(f'https://api-v2.soundcloud.com/stream/users/{soundcloud_user_id}')
        return all_playlists
    
    def handle_response(self,request,response,message,status_code):
        if request.path.startswith('/api/'):
            return Response({'message': message}, status=status_code)
        else:
            return self.redirect_admin(request,response,message)
        
    def redirect_admin(self,request,response,message):
        if response:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('admin:api_playlists_playlist_changelist')