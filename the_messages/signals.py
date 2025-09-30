from django.db.models.signals import post_save
from django.dispatch import receiver
from push_notifications.models import WebPushDevice
from the_messages.models import Message
import json

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Create the payload as a dictionary
        # payload = {
        #     "head": "New Message Added!",
        #     "body": f"Click to download latest message: {instance.name} now.",
        #     # Optional fields:
        #     "icon": "https://f005.backblazeb2.com/file/v-Studios/artifacts/logo+(2).png",
        #     "url": f"https://vickerdentstudios.com/messages/{instance.id}/",
        #     # "tag": "new-message",
        #     # "requireInteraction": False,
        # }
        payload = {
            "title": "New Message Added!",
            "message": f"Click to download latest message: {instance.name} now.",
            "icon": "https://f005.backblazeb2.com/file/v-Studios/artifacts/logo+(2).png",
            "url": f"https://vickerdentstudios.com/messages/{instance.id}/",
        }

        # Get all devices with the specific name
        devices = WebPushDevice.objects.filter(name="message_requests")

        # Send to each device individually (more reliable than bulk send)
        for device in devices:
            print(device)
            try:
                device.send_message(
                    message=json.dumps(payload),
                    ttl=3600  # Time to live in seconds
                )
                print(f"✓ Sent to device {device.id}") # type: ignore
            except Exception as e:
                print(f"Failed to send to device {device.registration_id}: {e}")
                # Print the full error for debugging
                import traceback
                traceback.print_exc()

