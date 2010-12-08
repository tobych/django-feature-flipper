from django import template
from django.template import NodeList

from featureflipper.models import Feature


register = template.Library()

@register.tag
def feature(parser, token):

    try:
        tag_name, feature = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    end_tag = 'endfeature'
    nodelist_enabled = parser.parse(('disabled', end_tag))
    token = parser.next_token()

    if token.contents == 'disabled':
        nodelist_disabled = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_disabled = NodeList()

    return FeatureNode(feature, nodelist_enabled, nodelist_disabled)


class FeatureNode(template.Node):

    def __init__(self, feature, nodelist_enabled, nodelist_disabled):
        self.feature = feature
        self.nodelist_enabled = nodelist_enabled
        self.nodelist_disabled = nodelist_disabled

    def render(self, context):

        try:
            feature = Feature.objects.get(name=self.feature)
            enabled = feature.enabled
        except Feature.DoesNotExist:
            enabled = False

        if enabled:
            return self.nodelist_enabled.render(context)
        else:
            return self.nodelist_disabled.render(context)
