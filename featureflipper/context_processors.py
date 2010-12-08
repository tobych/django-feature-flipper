from featureflipper.models import Feature

# Not sure if this needs to be thread-safe, as custom tags do


def features(request):
    """
    Returns context variables required by apps that use featureflipper.
    """
    return {
        'features': request.features
    }
