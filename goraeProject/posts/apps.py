from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'


    #시그널 등록 
    def ready(self):
        import posts.signals
