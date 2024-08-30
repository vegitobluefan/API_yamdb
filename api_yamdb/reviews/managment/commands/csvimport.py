import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    pass