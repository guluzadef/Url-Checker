from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Urls
import requests

print('HERE!!')


@receiver(post_save, sender=Urls)
def check_url(sender, instance, created, **kwargs):
    if created:
        print(instance)
        try:
            response = requests.get(instance.url)
            if response.status_code == 200:
                instance.status = True
                instance.save()
        except:
            pass
