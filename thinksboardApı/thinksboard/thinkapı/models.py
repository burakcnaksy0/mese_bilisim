from django.db import models


# Create your models here.

class UserLogInModel(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


from django.db import models


class TelemetryData(models.Model):
    device_uuid = models.UUIDField()
    temperature = models.FloatField()
    machine_state = models.FloatField()
    timestamp = models.DateTimeField()
