from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


CSV_FILES = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, file in CSV_FILES.items():
            with open(
                f'{settings.BASE_DIR}/data/{file}',
                encoding='utf-8'
            ) as csvfile:
                for row in DictReader(csvfile):
                    model.objects.get_or_create(**dict(row))
