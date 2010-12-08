from django.shortcuts import render_to_response
from django.template import RequestContext

from featureflipper.models import Feature


def index(request):

    message = "search=%s, login=%s, unknown=%s" % \
        (request.features['search'], request.features['login'],
         request.features['unknown'])

    return render_to_response('index.html', {'message': message},
        context_instance=RequestContext(request))
