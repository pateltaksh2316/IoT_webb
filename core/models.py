# Create your models here.
from django.db import models

class MqttLog(models.Model):
    topic = models.CharField(max_length=255)
    payload = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)  # ✅ REAL SERVER TIME

    def __str__(self):
        return f"{self.topic} @ {self.timestamp}"


# class SensorData(models.Model):
#     device_id = models.CharField(max_length=50)

#     temperature = models.FloatField(null=True, blank=True)
#     humidity = models.FloatField(null=True, blank=True)
#     light_sensor = models.IntegerField(null=True, blank=True)

#     total_height = models.FloatField(null=True, blank=True)
#     total_volume = models.FloatField(null=True, blank=True)
#     percentage = models.FloatField(null=True, blank=True)
#     filled_volume = models.FloatField(null=True, blank=True)

#     topic = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.device_id} @ {self.timestamp}"
