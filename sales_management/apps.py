from django.apps import AppConfig

class SalesManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_management'
    
    def ready(self):
        import sales_management.signals  # noqa
