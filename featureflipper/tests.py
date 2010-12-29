from django.test import TestCase
from django.http import HttpRequest
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from featureflipper.models import Feature
from featureflipper.middleware import FeaturesMiddleware

class featureflipperTest(TestCase):
    """
    Tests for django-feature-flipper
    """
    def test_something(self):
        feature = Feature.objects.create(name='fftestfeature')
        user = User.objects.create_user('fftestuser', '', 'password')

        c = Client()
        self.assertTrue(c.login(username='fftestuser', password='password'))

        response = c.get('/')
        self.assertTrue('features' in response.context)
        self.assertTrue('fftestfeature' in response.context['features'])
        self.assertFalse(response.context['features']['fftestfeature'])

        response = c.get('/?enable_fftestfeature')
        self.assertTrue(response.context['features']['fftestfeature'])

        response = c.get('/')
        self.assertFalse(response.context['features']['fftestfeature'])

        response = c.get('/?session_enable_fftestfeature')
        self.assertFalse(response.context['features']['fftestfeature'])

        perm = Permission.objects.get(codename='can_flip_with_url')
        user.user_permissions.add(perm)

        self.assertTrue(user.has_perm('featureflipper.can_flip_with_url'))
        response = c.get('/?session_enable_fftestfeature')

        self.assertTrue(response.context['features']['fftestfeature'])
        response = c.get('/')
        self.assertTrue(response.context['features']['fftestfeature'])

        response = c.get('/?session_clear_features')
        self.assertFalse(response.context['features']['fftestfeature'])

        feature.delete()
        user.delete()
