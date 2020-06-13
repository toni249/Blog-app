from django.apps import AppConfig


class BlogHomeConfig(AppConfig):
    name = 'blog_home'
    

    def ready(self):
    	import blog_home.signals