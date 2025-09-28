from django.db.models.signals import post_save
from django.dispatch import receiver
from webpush import send_group_notification
from the_messages.models import Message

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        payload = {
            "head": "New Message Added!",
            "body": "Hello World",
            "icon": "https://f005.backblazeb2.com/file/v-Studios/artifacts/logo+(2).png",
            "url": f"https://vickerdentstudios.com/messages/{instance.id}/"
        }

        send_group_notification(group_name="new_messages", payload=payload, ttl=1000)
