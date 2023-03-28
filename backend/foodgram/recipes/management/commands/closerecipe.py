from csv import DictReader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузить данные из data/ingredients.csv"

    def handle(self, *args, **options):
        print("Загрузка данных из ingredients.csv в Ingredient")
        model = Ingredient
        if model.objects.exists():
            print(
                f"{model.name} заполнена другими данными, отмена загрузки"
            )
        else:
            for row in DictReader(open(
                    "data/ingredients.csv", encoding="utf-8"
            )):
                model.objects.create(
                    name=row["ingredient"],
                    measurement_unit=row["measurement"]
                )
        print("Загрузка завершена")
