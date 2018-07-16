from django.db import models

# Create your models here.
class position_51(models.Model):
    id = models.AutoField(primary_key=True)
    up_time = models.CharField(max_length=300)
    position = models.CharField(max_length=300)
    pay = models.CharField(max_length=300)
    addr = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    url = models.CharField(max_length=300)

    class Meta:
        db_table = "position_51"