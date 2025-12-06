from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        # Import signals to ensure they are registered when Django starts
        try:
            import blog.signals  # noqa: F401
        except Exception:
            pass
