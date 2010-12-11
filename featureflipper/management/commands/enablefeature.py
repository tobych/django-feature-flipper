from django.core.management.base import BaseCommand

from featureflipper.models import Feature


class Command(BaseCommand):
    args = '[feature ...]'
    help = 'Enables the named features in the database.'

    def handle(self, *features, **options):
        for name in features:
            try:
                feature = Feature.objects.get(name=name)
            except Feature.DoesNotExist:
                print "Feature %s is not in the database." % name
                return
            else:
                if feature.enabled:
                    print "Feature %s is already enabled." % feature
                else:
                    feature.enable()
                    feature.save()
                    print "Enabled feature %s." % feature
