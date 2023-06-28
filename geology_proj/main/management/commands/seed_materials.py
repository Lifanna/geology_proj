"Габбро"
"Галечно-гравийные"
"Глина"
"Гнейсы"
"Гравий-песчано-гравийные"
"Гранит"
"Дресвяно-пеПесчано-дресвяные"
"Ил"
"Илисто-глинистые"
"Кристаллический сланец"
"ОКВ по габбро"
"ОКВ по гнейсам"
"ОКВ по гранитам"
"ОКВ по кристаллическим сланцам"
"ОКВ по сланцам"
"Песок"
"Песчано-илистые"
"ПКВ"
"ПРС-Торф"
"ПРС"
"Суглинок"
"Супесь-глинисто-песчаные"
"Щебнисто-галечн"
"Щебнисто-дресвяные"
from django.core.management.base import BaseCommand, CommandError
from main import models
import json


class Command(BaseCommand):
    def create_materials(self):
        models.LayerMaterial.objects.all().delete()
        with open('main/management/commands/entities_lookups/layerMaterials.json', mode="r", encoding="utf8") as file:
            layer_materials = json.load(file)

        for layer_material in layer_materials.get("layerMaterials"):
            new_layer_material = models.LayerMaterial(
                name = layer_material.get("name"),
                color = layer_material.get("color"),
            )

            new_layer_material.save()

    def handle(self, *args, **options):
        self.create_materials()
