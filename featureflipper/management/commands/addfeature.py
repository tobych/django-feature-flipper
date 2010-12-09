from django.core.management.base import BaseCommand

from featureflipper.models import Feature


class Command(BaseCommand):
    args = '[feature ...]'
    help = 'Adds the named features to the database, as disabled.'

    def handle(self, *features, **options):
        for name in features:
            try:
                feature = Feature.objects.get(name=name)
            except Feature.DoesNotExist:
                Feature.objects.create(name=name, enabled=False)
                print "Added feature %s" % name
            else:
                print "Feature %s already exists, and is %s" % (feature.name, feature.status)
