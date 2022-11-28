from django.dispatch import receiver
from django.db.models.signals import post_save

from note.models import Note


@receiver(post_save, sender=Note)
def check_empty_note(sender, instance, created, **kwargs):
    if instance.title == '' and instance.body == '':
        instance.delete()
