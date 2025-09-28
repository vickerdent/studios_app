from django.apps import AppConfig


class TheMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_messages'

    def ready(self) -> None:
        import the_messages.signals  # noqa: F401
