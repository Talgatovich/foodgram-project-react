import json

from django.core.management.base import BaseCommand

from recipes.models import Ingridient  # isort: skip


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open("../data/ingredients.json", "rb") as f:
            data = json.load(f)

            for val in data:
                inredient = Ingridient()
                inredient.name = val["name"]
                inredient.measurement_unit = val["measurement_unit"]
                inredient.save()
        print("finished")
