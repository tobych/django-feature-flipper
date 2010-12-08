from django.shortcuts import render_to_response
from django.template import RequestContext

from featureflipper.models import Feature
from featureflipper.signals import feature_defaulted


# This shows us how to receive the signal sent when a feature is
# defaulted to disabled. You might raise an exception here, or add the
# feature to the database.

def my_callback(sender, **kwargs):
        print "Feature '%s' defaulted!" % kwargs['feature']
feature_defaulted.connect(my_callback)

def index(request):

    message = "search=%s, login=%s, unknown=%s" % \
        (request.features['search'], request.features['login'],
         request.features['unknown'])

    return render_to_response('index.html', {'message': message},
        context_instance=RequestContext(request))
