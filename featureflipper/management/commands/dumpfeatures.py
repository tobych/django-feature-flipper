from django.core.management.base import BaseCommand
from django.utils import simplejson
from django.conf import settings

from featureflipper.models import Feature


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Output the features in the database in JSON format.'

        features = Feature.objects.all().values('name', 'description', 'enabled')

        # This doesn't guarantee any particular ordering of keys in each dictionary
        # values() doesn't do that, and simplejson's sort_keys just uses alpha sort

        print simplejson.dumps(list(features), indent=2)
