from django.db import models
from Server.Game import createSnapshot

class SnapshotModel(models.Model):
    SERVER_INDEX = models.IntegerField()
    CLIENT_INDEX = models.IntegerField()
    MODIFIED = models.DateTimeField(auto_now_add = True)
    X_COORD = models.FloatField()
    Y_COORD = models.FloatField()
    DEGREE = models.FloatField()
    SCORE = models.IntegerField()


#create an instance with every snapshot
