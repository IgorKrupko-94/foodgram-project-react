from csv import DictReader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузить данные из data/ingredients.csv"

    def handle(self, *args, **options):
        print("Загрузка данных из ingredients.csv в Ingredient")
        if Ingredient.objects.exists():
            print('Модель ингредиентов заполнена другими данными, '
                  'отмена загрузки')
        else:
            for row in DictReader(
                    open("data/ingredients.csv", encoding="utf-8")
            ):
                name, measurement = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement
                )
        print("Загрузка завершена")
