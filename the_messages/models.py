import os
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

from storages import FileStorage

UPCOMING = "UC"
COMPLETED = "C"
ONGOING = "OG"

STATUS_CHOICES = [
    (UPCOMING, "Upcoming"),
    (ONGOING, "Ongoing"),
    (COMPLETED, "Completed")
]

MEDIA_TYPES = [
    ("Audio", "Audio"),
    ("Video", "video"),
]

SESSIONS = [
    ("Morning", "Morning"),
    ("Evening", "Evening"),
    ("Night", "Night"),
]

@deconstructible
class GenerateMessageThumbnailPath:
    def __init__(self):
        pass

    def __call__(self, instance, filename):
       ext = filename.split('.')[-1]
       path = f"messages/{instance.id}/images"
       name = f"{instance.id}.{ext}"
       return os.path.join(path, name)

message_thumbnail_path = GenerateMessageThumbnailPath()

@deconstructible
class GenerateAttachmentPath:
    def __init__(self):
        pass

    def __call__(self, instance, filename):
       ext = filename.split('.')[-1]
       path = f"messages/{instance.message.id}/attachments"
       name = f"{instance.message.name} by {instance.message.author.name}.{ext}"
       return os.path.join(path, name)

attachment_path = GenerateAttachmentPath()

# Create your models here.
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    thumbnail = models.ImageField(upload_to=message_thumbnail_path, storage=FileStorage, blank=True, null=True)
    media_types = models.ManyToManyField('MediaType', related_name='messages')
    author = models.ForeignKey('Author', on_delete=models.PROTECT, related_name='messages')
    part_of_group = models.BooleanField(default=False)
    message_group = models.ForeignKey('MessageGroup', on_delete=models.SET_NULL, related_name='messages', blank=True, null=True)
    session = models.CharField(max_length=100, choices=SESSIONS, blank=True, null=True)  # e.g., "Morning", "Evening"
    is_sunday_service = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    message_length = models.CharField(max_length=7)  # e.g., "45:23"
    category = models.CharField(max_length=75, blank=True, null=True)  # e.g., "Kingdom Stewardship"
    video_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.name} by {self.author.name}"

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="160" height="90" />')
        return ""

    # Link to upload audio attachment if none else show display attachment
    @property
    def attachment_preview(self):
        if self.attachments.count() == 0: # type: ignore
            return mark_safe(f'<a href="/messages/{self.id}/upload_audio/">Upload Audio</a>')
        else:
            return mark_safe(
                f'<audio controls name="media"><source src="{self.attachments.all()[0].file.url}" type="audio/mpeg"></audio>' # type: ignore
            )

class MessageGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='group_thumbnails/', storage=FileStorage, blank=True, null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='message_groups')
    is_conference = models.BooleanField(default=False)
    conference_name = models.CharField(max_length=255, blank=True, null=True)
    conference_tag = models.CharField(max_length=30, blank=True, null=True)
    month = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_speakers = models.IntegerField(default=1)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=UPCOMING)

    def __str__(self):
        return self.name

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" width="160" height="90" />')
        return ""

class MediaType(models.Model):
  type_name = models.CharField(max_length=10, choices=MEDIA_TYPES, unique=True, default="Audio")

  def __str__(self):
    return self.type_name

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    media_type = models.ForeignKey(MediaType, on_delete=models.PROTECT, related_name='attachments')
    file = models.FileField(upload_to=attachment_path, storage=FileStorage, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.media_type.type_name.lower() == 'audio':
            allowed_extensions = ['mp3', 'aac', 'wav', 'aiff', 'flac', 'alac']
        else:
            allowed_extensions = ['mp4', 'mov', 'avi', 'mkv', 'wmv']
        validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
        validator(self.file)

    def __str__(self):
        return f"Attachment for {self.message} - {self.id} - {self.media_type.type_name}"

    @property
    def sound_display(self):
        if self.file and self.media_type.type_name == 'audio':
            return mark_safe(f'<audio controls name="media"><source src="{self.file.url}" type="audio/mpeg"></audio>')
        return ""

class Author(models.Model):
    name = models.CharField(max_length=255)
    brief_desc = models.CharField(max_length=72)
    biography = models.TextField()
    photo = models.ImageField(upload_to='author_photos/', storage=FileStorage, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def photo_display(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="100" height="100" />')
        return ""

class Comment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # A like is linked to a session
    session = models.OneToOneField('Session', on_delete=models.CASCADE, related_name='likes', blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.user_name} on {self.message.name}"

class Session(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_id
