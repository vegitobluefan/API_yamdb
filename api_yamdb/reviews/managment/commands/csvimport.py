import csv
import os

from django.core.management.base import BaseCommand
from api_yamdb import settings

from reviews.models import (Category, Comment, Genre, Review, Title, User)


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_files = {
            'category.csv': Category,
            'comments.csv': Comment,
            'genre.csv': Genre,
            'review.csv': Review,
            'titles.csv': Title,
            'users.csv': User,
        }

        for csv_file, model in csv_files.items():
            with open(os.path.join(
                settings.BASE_DIR, 'static/data/', csv_file
            ), encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    model.objects.create(**row)
