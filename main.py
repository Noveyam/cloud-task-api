import os

from django.core.asgi import get_asgi_application

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    return get_asgi_application()

app = main()