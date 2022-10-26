from django.db import models
from base_user.models import MyUser


# Create your models here.

class Urls(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_url')
    url = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.url}'

    class MPTTMeta:
        order_insertion_by = ['id']

    class Meta:
        verbose_name = 'UrlTable'
        verbose_name_plural = 'Urls Table'

