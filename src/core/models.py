from django.db import models

class AbstractTrack(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True