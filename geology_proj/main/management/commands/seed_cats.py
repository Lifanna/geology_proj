import main.models as main_models
import main.custom_models.good_models as good_models
import json


def create_feed_types():
    good_models.FeedType.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsFeedTypes.json', mode="r", encoding="utf8") as file:
        feed_types = json.load(file)

    for feed_type in feed_types.get("catsFeedTypes"):
        new_feed_type = good_models.FeedType(
            name = feed_type.get("name"),
            pet = good_models.Pet.objects.get(name=feed_type.get("pet")),
        )

        new_feed_type.save()

def create_brands():
    good_models.Brand.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsBrands.json', mode="r", encoding="utf8") as file:
        cats_brands = json.load(file)

    for cats_brand in cats_brands.get("catsBrands"):
        new_cats_brand = good_models.Brand(
            name = cats_brand.get("name"),
            pet = good_models.Pet.objects.get(name=cats_brand.get("pet")),
        )

        new_cats_brand.save()

def create_feeds():
    pass

def create_pet_ages():
    good_models.PetAge.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsAges.json', mode="r", encoding="utf8") as file:
        cats_ages = json.load(file)

    for cats_age in cats_ages.get("catsAges"):
        new_cats_age = good_models.PetAge(
            name = cats_age.get("name"),
        )

        new_cats_age.save()

def create_pet_sizes():
    good_models.Size.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsSizes.json', mode="r", encoding="utf8") as file:
        cats_sizes = json.load(file)

    for cats_size in cats_sizes.get("catsSizes"):
        new_cats_size = good_models.Size(
            name = cats_size.get("name"),
        )

        new_cats_size.save()

def create_ingredients():
    good_models.Ingredient.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsIngredients.json', mode="r", encoding="utf8") as file:
        cats_ingredients = json.load(file)

    for cats_ingredient in cats_ingredients.get("catsIngredients"):
        new_cats_ingredient = good_models.Ingredient(
            name = cats_ingredient.get("name"),
        )

        new_cats_ingredient.save()

def create_special_series():
    good_models.SpecialSeries.objects.all().delete()
    with open('main/management/commands/entities_lookups/cats/catsSpecialSeries.json', mode="r", encoding="utf8") as file:
        cats_special_series = json.load(file)

    for cats_special_serie in cats_special_series.get("catsSpecialSeries"):
        new_cats_special_serie = good_models.SpecialSeries(
            name = cats_special_serie.get("name"),
        )

        new_cats_special_serie.save()
