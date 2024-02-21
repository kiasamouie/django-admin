import os
from django.contrib import admin
from django.urls import path
from .viewsets import PlaylistViewSet
from .models import Playlist
from api.socials.models import Social, SocialPlatform, SocialPlatformMapping

class PlaylistAdmin(admin.ModelAdmin):
    change_list_template = os.path.join('..','templates','change_list.html')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # extra_context['soundcloud_urls'] = Social.objects.exclude(soundcloud_url__isnull=True).exclude(soundcloud_url__exact='').values_list('soundcloud_url', flat=True).distinct()
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fetch_urls/', PlaylistViewSet().fetch_urls, name='fetch_urls'),
        ]
        return custom_urls + urls
    
admin.site.register(Playlist,PlaylistAdmin)
admin.site.register(SocialPlatform)
admin.site.register(SocialPlatformMapping)