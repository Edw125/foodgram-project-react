import csv
from django.db import Error
from django.core.management.base import BaseCommand, CommandError

from backend.settings import MEDIA_ROOT
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Uploading files to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ingredients',
            action='store_true',
            help='add_ingredients',
        )
        parser.add_argument(
            '--tags',
            action='store_true',
            help='add_tags',
        )

    def handle(self, *args, **options):
        if options['ingredients']:
            path = MEDIA_ROOT + '/import/ingredients.csv'
            with open(path, 'r', newline='') as ingredients:
                ingredients = csv.reader(ingredients)
                try:
                    for ingredient in ingredients:
                        Ingredient.objects.create(
                            name=ingredient[0], measurement_unit=ingredient[1])
                    self.stdout.write(self.style.SUCCESS(
                        'File ingredients.csv uploaded in database successfully'
                    ))
                except Error:
                    raise CommandError(
                        'Some error occurred while creating the object "ingredient"'
                    )

        if options['tags']:
            path = MEDIA_ROOT + '/import/tags.csv'
            with open(path, 'r', newline='') as tags:
                tags = csv.reader(tags)
                try:
                    for tag in tags:
                        Tag.objects.create(
                            name=tag[0], hex_color=tag[1], slug=tag[2])
                    self.stdout.write(self.style.SUCCESS(
                        'File tags.csv uploaded in database successfully'
                    ))
                except Error:
                    raise CommandError(
                        'Some error occurred while creating the object "tag"'
                    )
