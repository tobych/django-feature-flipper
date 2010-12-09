from django.test import TestCase

from featureflipper.models import Feature
from featureflipper.middleware import FeaturesMiddleware
from featureflipper.management import load_features_from_json_file

import os

class featureflipperTest(TestCase):
    """
    Tests for django-featureflipper
    """

    file = os.path.abspath(os.path.dirname(__file__)) + "/test_features.json"

    def setUp(self):
        Feature.objects.all().delete()

    def test_features_from_database(self):
        Feature.objects.create(name='one')
        m = FeaturesMiddleware()
        features = dict(m.features_from_database())
        self.assertTrue('one' in features)
        self.assertEquals(features['one'], False)

    def test_load_features_from_json_file(self):
        load_features_from_json_file(self.file)
        features = Feature.objects.all()

        self.assertEquals(len(features), 2)

        feature = Feature.objects.get(name="login")
        self.assertEquals(feature.enabled, True)
        self.assertEquals(feature.description, "Login link")

        feature = Feature.objects.get(name="search")
        self.assertEquals(feature.enabled, False)
        self.assertEquals(feature.description, "Search box")

    def test_features_from_json_file_overwrite_existing(self):
        Feature.objects.create(name='login', enabled=False)
        f = Feature.objects.get(name='login')
        self.assertEquals(f.enabled, False)
        
        load_features_from_json_file()

        f = Feature.objects.get(name='login')
        self.assertEquals(f.enabled, True)
