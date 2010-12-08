from featureflipper.models import Feature

import re


class FeaturesMiddleware(object):

    # Matches per-request flipper in URL
    _REQUEST_ENABLE = re.compile("^enable_(?P<feature>[a-zA-Z_]+)$")

    # Matches per-session flipper in URL
    _SESSION_ENABLE = re.compile("^session_enable_(?P<feature>[a-zA-Z_]+)$")

    # Mathes flipper we put in the session
    _FEATURE_STATUS = re.compile("^feature_status_(?P<feature>[a-zA-Z_]+)$")

    def process_request(self, request):

        if 'session_clear_features' in request.GET:
            self.clear_features_from_session(request.session)

        # 1. Collect features from the database
        features = self.features_from_database()

        # 2. Collect features from the session
        features.update(self.features_from_session(request.session))

        # 3. Collect features from the URL that must persist across the session
        session_features = self.session_features_from_url(request.GET)
        features.update(session_features)

        # 4. Add these to the session so they persist
        for feature in session_features:
            self.add_feature_to_session(request.session, feature)

        # 5. Collect features from request.GET that are just for this request
        features.update(self.features_from_url(request.GET))

        request.features = FeatureDict(features)

        return None

    def features_from_database(self):
        features = {}
        for feature in Feature.objects.all():
            features[feature.name] = feature.enabled
        return features

    def features_from_session(self, session):
        """Provides a dictionary of feature names and True/False"""
        features = {}
        for key in session.keys():
            m = re.match(self._FEATURE_STATUS, key)
            if m:
                feature = m.groupdict()['feature']
                if session[key] == 'enabled':
                    features[feature] = True
                else: # We'll assume it's disabled
                    features[feature] = False
        return features

    def features_from_url(self, get):
        """Provides a dictionary of feature names and True/False"""
        features = {}
        for parameter in get:
            m = re.match(self._REQUEST_ENABLE, parameter)
            if m:
                feature = m.groupdict()['feature']
                features[feature] = True
        return features

    def session_features_from_url(self, get):
        """Provides a dictionary of feature names and True/False"""
        features = {}
        for parameter in get:
            m = re.match(self._SESSION_ENABLE, parameter)
            if m:
                feature = m.groupdict()['feature']
                features[feature] = True
        return features

    def add_feature_to_session(self, session, feature):
        session["feature_status_" + feature] = 'enabled'

    def clear_features_from_session(self, session):
        for key in session.keys():
            if re.match(self._FEATURE_STATUS, key):
                del session[key]


class FeatureDict(dict):

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            return False
