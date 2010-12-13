from django.conf import settings

from featureflipper.models import Feature
from featureflipper.signals import feature_defaulted
from featureflipper import FeatureProvider

import re

# Per-request flipper in URL
_REQUEST_ENABLE = re.compile("^enable_(?P<feature>\w+)$")

# Per-session flipper in URL
_SESSION_ENABLE = re.compile("^session_enable_(?P<feature>\w+)$")

# Flipper we put in the session
_FEATURE_STATUS = re.compile("^feature_status_(?P<feature>\w+)$")


class FeaturesMiddleware(object):

    def process_request(self, request):
        panel = FeaturesPanel()
        panel.add('site', list(self.features_from_database(request)))

        for plugin in FeatureProvider.plugins:
            panel.add(plugin.source, list(plugin.features(request)))

        if getattr(settings, 'FEATURE_FLIPPER_ANONYMOUS_URL_FLIPPING', False) or \
                request.user.has_perm('can_flip_with_url'):
            if 'session_clear_features' in request.GET:
                self.clear_features_from_session(request.session)
            for feature in dict(self.session_features_from_url(request)):
                self.add_feature_to_session(request.session, feature)

        panel.add('session', list(self.features_from_session(request)))
        panel.add('url', list(self.features_from_url(request)))

        request.features = FeatureDict(panel.states())
        request.features_panel = panel

        return None

    def features_from_database(self, request):
        """Provides an iterator yielding tuples (feature name, True/False)"""
        for feature in Feature.objects.all():
            yield (feature.name, feature.enabled)

    def features_from_session(self, request):
        """Provides an iterator yielding tuples (feature name, True/False)"""
        for key in request.session.keys():
            m = re.match(_FEATURE_STATUS, key)
            if m:
                feature = m.groupdict()['feature']
                if request.session[key] == 'enabled':
                    yield (feature, True)
                else: # We'll assume it's disabled
                    yield (feature, False)

    def features_from_url(self, request):
        """Provides an iterator yielding tuples (feature name, True/False)"""
        for parameter in request.GET:
            m = re.match(_REQUEST_ENABLE, parameter)
            if m:
                yield (m.groupdict()['feature'], True)

    def session_features_from_url(self, request):
        """Provides an iterator yielding tuples (feature name, True/False)"""
        for parameter in request.GET:
            m = re.match(_SESSION_ENABLE, parameter)
            if m:
                feature = m.groupdict()['feature']
                yield (feature, True)

    def add_feature_to_session(self, session, feature):
        session["feature_status_" + feature] = 'enabled'

    def clear_features_from_session(self, session):
        for key in session.keys():
            if re.match(_FEATURE_STATUS, key):
                del session[key]


class FeatureDict(dict):

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            feature_defaulted.send(sender=self, feature=key)
            return False

class FeaturesPanel():

    def __init__(self):
        self._features = {}
        self._sources = []

    def add(self, source, features):
        self._sources.append((source, features))
        for (feature, enabled) in features:
            self._features[feature] = {'enabled': enabled, 'source': source}

    def enabled(self, name):
        return self._features[name]['enabled']

    def source(self, name):
        return self._features[name]['source']

    def states(self):
        # Returns a dictionary, mapping each feature name to its (final) state.
        return dict([(x, y['enabled']) for x, y in self._features.items()])
