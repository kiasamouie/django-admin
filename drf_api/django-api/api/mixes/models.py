from django.db import models
# from api.playlists.models import Playlist

class MixesManager(models.Manager):
    def create_mix(self, name, url):
        """
        Creates and saves a new mix.
        """
        mix = self.model(name=name, url=url)
        mix.save(using=self._db)
        return mix

class Mix(models.Model):
    title = models.CharField("Title", max_length=240)
    playlist = models.ForeignKey("api_playlists.Playlist", on_delete=models.CASCADE)

    objects = MixesManager()

    def __str__(self):
        return self.title