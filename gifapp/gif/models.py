from django.db import models

# Create your models here.
class gif_init(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    class Meta:
        db_table = "gif_init"