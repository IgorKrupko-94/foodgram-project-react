import os
from csv import reader

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузить данные из data/ingredients.csv"

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            default='ingredients.csv',
            nargs='?',
            type=str
        )

    def handle(self, *args, **options):
        print("Загрузка данных из ingredients.csv в Ingredient")
        if Ingredient.objects.exists():
            print('Модель ингредиентов заполнена другими данными, '
                  'отмена загрузки')
        else:
            with open(os.path.join(
                    settings.BASE_DIR,
                    'data',
                    options['filename']),
                    'r',
                    encoding='utf-8'
            ) as file_name:
                data = reader(file_name)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
        print("Загрузка завершена")
