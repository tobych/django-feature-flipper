from django.shortcuts import render_to_response
from django.template import RequestContext

from featureflipper.models import Feature
from featureflipper.signals import feature_defaulted


# We use the feature_defaulted signal to print a simple message
# warning that a feature has been defaulted to disabled. You might
# instead raise an exception here (to help avoid bugs in templates),
# or add the feature to the database.

def my_callback(sender, **kwargs):
        print "Feature '%s' defaulted!" % kwargs['feature']
feature_defaulted.connect(my_callback)

def index(request):
    message = "search=%s, profile=%s, unknown=%s" % \
	(request.features['search'], request.features['profile'],
         request.features['unknown'])
    return render_to_response('featureflipper_example/index.html', {'message': message},
        context_instance=RequestContext(request))
