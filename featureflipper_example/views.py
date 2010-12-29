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

# Uncomment the following line to enable this:
# feature_defaulted.connect(my_callback)


def index(request):
    # We'll include all the features, just so we can show all the details in the page
    feature_list = Feature.objects.all()
    # Below, we'll also include the features_panel in the context.
    # 'features' will already be added to the context by the middleware.
    return render_to_response('featureflipper_example/index.html',
        {'features_panel': request.features_panel, 'feature_list': feature_list},
        context_instance=RequestContext(request))
