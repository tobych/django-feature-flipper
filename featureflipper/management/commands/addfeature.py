from django.core.management.base import BaseCommand
from django.core.management import call_command

from featureflipper.models import Feature


class Command(BaseCommand):
    args = ''
    help = 'Adds the named feature to the database, as disabled'

    def handle(self, name, *args, **options):
        Feature.objects.create(name=name, enabled=False)
        print "Added feature %s" % name
