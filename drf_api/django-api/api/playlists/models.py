from django.db import models

class PlaylistsManager(models.Manager):
    def get_featured_playlists(self):
        return self.filter(is_featured=True)

    def create_playlist(self, title, url):
        """
        Creates and saves a new playlist.
        """
        playlist = self.model(title=title, url=url)
        playlist.save(using=self._db)
        return playlist

class Playlist(models.Model):
    title = models.CharField("Title", max_length=240)
    permalink_url = models.URLField("PermalinkUrl", max_length=240)
    artwork_url = models.URLField("ArtworkURL", max_length=240)
    sc_playlist_id = models.IntegerField("SoundcloudPlaylistID")
    duration = models.IntegerField("Duration")
    track_count = models.IntegerField("TrackCount")

    objects = PlaylistsManager()

    def __str__(self):
        return self.title