# Generated by Django 3.2.13 on 2023-12-05 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240, verbose_name='Title')),
                ('permalink_url', models.URLField(max_length=240, verbose_name='PermalinkUrl')),
                ('artwork_url', models.URLField(max_length=240, verbose_name='ArtworkURL')),
                ('sc_playlist_id', models.IntegerField(verbose_name='SoundcloudPlaylistID')),
                ('duration', models.IntegerField(verbose_name='Duration')),
                ('track_count', models.IntegerField(verbose_name='TrackCount')),
            ],
        ),
    ]