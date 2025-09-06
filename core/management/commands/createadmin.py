from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='Gacho').exists():
            User.objects.create_superuser(
                username='Gacho',
                email='gachoyasamuel37@gmail.com',
                password='Samuel9$'
            )
            self.stdout.write(self.style.SUCCESS('Gacho user created'))
        else:
            self.stdout.write(self.style.WARNING('Gacho user already exists'))
