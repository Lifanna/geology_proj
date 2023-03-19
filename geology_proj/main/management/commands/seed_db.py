from django.core.management.base import BaseCommand, CommandError
import main.models as main_models
import main.custom_models.good_models as good_models
import json
from django.core.files.base import ContentFile
from . import seed_cats


class Command(BaseCommand):
    def create_roles(self):
        main_models.Role.objects.get_or_create(title="администратор")
        main_models.Role.objects.get_or_create(title="продавец")
        main_models.Role.objects.get_or_create(title="потребитель")

    def create_pets(self):
        good_models.Pet.objects.all().delete()
        with open('main/management/commands/entities_lookups/petLookup.json', mode="r", encoding="utf8") as file:
            pets = json.load(file)

        for pet in pets.get("pets"):
            new_pet = good_models.Pet(
                name = pet.get("name"),
                description_text = pet.get("descriptionText"),
                url = pet.get("url"),
            )

            with open(pet.get("image"), mode='rb') as f:
                data = f.read()

            new_pet.image.save(pet.get("imageFilename"), ContentFile(data))

            new_pet.save()

    def create_good_types(self):
        good_models.GoodType.objects.all().delete()
        with open('main/management/commands/entities_lookups/goodTypes.json', mode="r", encoding="utf8") as file:
            good_types = json.load(file)

        for good_type in good_types.get("goodTypes"):
            new_good_type = good_models.GoodType(
                name = good_type.get("name"),
                pet = good_models.Pet.objects.get(name=good_type.get("pet")),
                alias = good_type.get("alias"),
                url = good_type.get("url"),
            )

            with open(good_type.get("image"), mode='rb') as f:
                data = f.read()

            new_good_type.image.save(good_type.get("imageFilename"), ContentFile(data))

            new_good_type.save()

    def create_packet_types(self):
        good_models.PacketType.objects.all().delete()
        with open('main/management/commands/entities_lookups/packetTypes.json', mode="r", encoding="utf8") as file:
            packet_types = json.load(file)

        for packet_type in packet_types.get("packetTypes"):
            new_packet_type = good_models.PacketType(
                name = packet_type.get("name"),
            )

            new_packet_type.save()

    def handle(self, *args, **options):
        self.create_roles()
        self.create_pets()
        self.create_good_types()
        self.create_packet_types()
        seed_cats.create_feed_types()
        seed_cats.create_brands()
        seed_cats.create_pet_ages()
        seed_cats.create_pet_sizes()
        seed_cats.create_ingredients()
        seed_cats.create_special_series()
