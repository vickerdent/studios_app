from django.conf import settings
from django_backblaze_b2 import BackblazeB2Storage
from django.core.files.storage import FileSystemStorage

FileStorage = (
    BackblazeB2Storage()
    if settings.USE_CLOUD_STORAGE
    else FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
)
