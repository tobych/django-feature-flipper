from django.core.management.base import BaseCommand
from django.core.management import call_command

from featureflipper.models import Feature


class Command(BaseCommand):
    args = ''
    help = 'Lists each feature defined in the database, and its status'

    def handle(self, *args, **options):
        for feature in Feature.objects.all():
            print "%s is %s" % (feature.name, feature.status)
