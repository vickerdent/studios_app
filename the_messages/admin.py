from django.contrib import admin
from .models import Message, Author, MediaType, MessageGroup, Attachment, Comment

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'thumbnail_preview')
    search_fields = ('name', 'description', 'author__name')
    list_filter = ('date', 'author', 'media_types', 'is_featured', 'is_sunday_service', 'session')
    list_display = ('name', 'author', 'date', 'is_featured', 'is_sunday_service', 'session', 'thumbnail_preview')
    ordering = ('-date',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

class MessageGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at')
    search_fields = ('name', 'description', 'author__name', 'conference_name', 'conference_tag', 'location')
    list_filter = ('is_conference', 'month', 'author')
    list_display = ('name', 'is_conference', 'conference_tag', 'month', 'status', 'start_date', 'end_date', 'thumbnail_preview')
    ordering = ('-created_at',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'uploaded_at')
    search_fields = ('message__name', 'file__name')
    list_display = ('message', 'media_type', 'uploaded_at', 'sound_display')
    list_filter = ('media_type', 'uploaded_at')
    ordering = ('-uploaded_at',)

    def sound_display(self, obj):
        return obj.sound_display

    sound_display.short_description = 'Audio Preview'
    sound_display.allow_tags = True

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    list_display = ('name', 'brief_desc', 'photo_preview')

    def photo_preview(self, obj):
        return obj.photo_display

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True

admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(MediaType)
admin.site.register(Comment)
admin.site.register(MessageGroup, MessageGroupAdmin)
