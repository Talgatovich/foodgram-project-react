from django.http.response import HttpResponse, HttpResponseNotFound


def create_ingredients_list(recipes_in_cart):
    ingridients = {}
    for obj in recipes_in_cart:
        recipe = obj.recipe.recipe
        for val in recipe.all():
            name = val.ingredient.name
            amount = val.amount
            measurement_unit = val.ingredient.measurement_unit
            if name not in ingridients:
                ingridients[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                ingridients[name]["amount"] += amount

    with open("./api/Ingredients_list.txt", "w", encoding="utf-8") as file:
        for key in ingridients:
            file.write(
                (
                    f'{key} - {ingridients[key]["amount"]} '
                    f'{ingridients[key]["measurement_unit"]} \n'
                )
            )


def dowload_list(file_location):
    try:
        with open(file_location, "r", encoding="utf-8") as f:
            file_data = f.read()

        response = HttpResponse(file_data, content_type="text/plain")
        response[
            "Content-Disposition"
        ] = 'attachment; filename="Ingredients_list.txt"'
    except IOError:
        response = HttpResponseNotFound("<h1>File not exist</h1>")
    return response
