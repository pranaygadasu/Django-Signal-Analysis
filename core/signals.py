import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel

@receiver(post_save, sender=TestModel)
def my_signal(sender, instance, **kwargs):
    print("Signal started")

    print("Signal Thread:", threading.get_ident())

    time.sleep(5)

    print("Signal finished")