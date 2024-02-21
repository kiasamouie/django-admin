from django.db import models

class SocialPlatform(models.Model):
    name = models.CharField("Platform Name", max_length=50, unique=True)
    base_url = models.URLField("Base URL")  # Store the base URL common to each platform

    def __str__(self):
        return self.name

class Social(models.Model):
    handle = models.CharField("Handle", max_length=240)
    platforms = models.ManyToManyField(SocialPlatform, through='SocialPlatformMapping')

    def __str__(self):
        return self.handle

class SocialPlatformMapping(models.Model):
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    platform = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE)
    platform_url = models.CharField("Platform URL", max_length=100)  # Store platform-specific ID or handle
    platform_identifier  = models.CharField("Platform ID", max_length=100)  # Store platform-specific ID or handle

    def __str__(self):
        return f"{self.social.handle} - {self.platform.name}"
