from django.db import models
import datetime
from django.utils import timezone


class snapshotModel(models.Model):
    SERVER_INDEX = models.IntegerField()
    CLIENT_INDEX = models.IntegerField()
    SCORE = models.IntegerField()
    MODIFIED = models.DateTimeField("Created now: ")

    def createdNow(self):
        return self.modified >= timezone.now() - datetime.timedelta(days=1)

# Create your models here.
