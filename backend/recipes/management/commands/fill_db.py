import json
from itertools import count

from django.core.management.base import BaseCommand
from recipes.models import Ingridients


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open("../data/ingredients.json", "rb") as f:
            data = json.load(f)

            for val in data:
                inredient = Ingridients()
                inredient.name = val["name"]
                inredient.measurement_unit = val["measurement_unit"]
                inredient.save()
        print("finished")
