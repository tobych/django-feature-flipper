from featureflipper.models import Feature

import re


class FeaturesMiddleware(object):

    # This stuff should only be enabled with certain permissions

    # I think all this should be good at *disabling* stuff too, as removing stuff
    # from UI is so important so often. So let's allow the turtle to be disabled.
    # {% feature turtle enabled %}<img ...>{% endfeature %}
    # Now, we certainly need to clearly define the precedence. That 'enabled' will
    # override the usual default of 'disabled'.
    # We should also easily be able to override whatever's in the database in settings.py,
    # eg for the dev environment so we don't have to piss about with the database just to
    # get a feature showing.

    def process_request(self, request):

        request.feature = FeatureDict()

        feature_status = re.compile("^feature_status_(?P<feature>[a-zA-Z_]+)$")
        if 'session_clear_features' in request.GET:
            for key in request.session.keys():
                m = re.match(feature_status, key)
                if m:
                    del request.session[key]
                    print "deleted %s" % key
        else:
            for key in request.session.keys():
                m = re.match(feature_status, key)
                if m:
                    feature = m.groupdict()['feature']
                    if request.session[key] == 'enabled':
                        request.feature[feature] = True
                    else: # We'll assume it's disabled
                        request.feature[feature] = False
                
        enable = re.compile("^enable_(?P<feature>[a-zA-Z_]+)$")
        session_enable = re.compile("^session_enable_(?P<feature>[a-zA-Z_]+)$")
        for parameter in request.GET:

            m = re.match(enable, parameter)
            if m:
                feature = m.groupdict()['feature']
                request.feature[feature] = True
                continue

            m = re.match(session_enable, parameter)
            if m:
                feature = m.groupdict()['feature']
                request.feature[feature] = True
                request.session["feature_status_" + feature] = 'enabled'

        return None

class FeatureDict():

    def __init__(self):
        self._cache = {}

    def __getitem__(self, key):
        if key in self._cache:
            enabled = self._cache[key]
        else:
            try:
                feature = Feature.objects.get(name=key)
                enabled = feature.enabled
                self._cache[key] = enabled
            except Feature.DoesNotExist:
                enabled = False
        return enabled

    def __setitem__(self, key, value):
        self._cache[key] = value
