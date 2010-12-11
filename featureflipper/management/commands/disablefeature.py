from django.core.management.base import BaseCommand

from featureflipper.models import Feature


class Command(BaseCommand):
    args = '[feature ...]'
    help = 'Disables the named features in the database.'

    def handle(self, *features, **options):
        for name in features:
            try:
                feature = Feature.objects.get(name=name)
            except Feature.DoesNotExist:
                print "Feature %s is not in the database." % name
                return
            else:
                if not feature.enabled:
                    print "Feature %s is already disabled." % feature
                else:
                    feature.disable()
                    feature.save()
                    print "Disabled feature %s." % feature
