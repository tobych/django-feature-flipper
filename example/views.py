from django.shortcuts import render_to_response
from django.template import RequestContext

from featureflipper.models import Feature


def index(request):

    if request.feature['search']:
        message = "Search is ENABLED"
    else:
        message = "Search is DISABLED"

    return render_to_response('index.html', {'message': message},
        context_instance=RequestContext(request))
