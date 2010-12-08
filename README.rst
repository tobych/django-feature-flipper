======================
Django Feature Flipper
======================

Use this pluggable application to flip features of your Django site on
and off, so you can deploy code and schema changes for upcoming
features but hide them from your users until you're ready.

This is one practice commonly used in `continuous deployment`.

The term "feature flipper" seems to have come from Flickr, as
described in this often-cited blog post:

http://code.flickr.com/blog/2009/12/02/flipping-out/

django-feature-flipper is in part inspired by that post, along with
some of the other feature flippers available, including:

- https://github.com/qype/feature_flipper (for Rails, by Florian Munz at Qype)
- https://github.com/grillpanda/dolphin (for Rails, by Matt Johnson)

More on feature flippers:

- http://old.nabble.com/Feature-Flipper-to30400696.html 
- http://www.alandelevie.com/2010/05/19/feature-flippers-with-rails/
- http://engineering.qype.com/2010/06/03/how-we-work-flipping-features/ (also Florian Munz)

Continuous deployment:

- http://www.startuplessonslearned.com/2009/06/why-continuous-deployment.html
- http://timothyfitz.wordpress.com/2009/02/10/continuous-deployment-at-imvu-doing-the-impossible-fifty-times-a-day/
- http://radar.oreilly.com/2009/03/continuous-deployment-5-eas.html
- http://en.wikipedia.org/wiki/Lean_Startup


Installation
============

#. Add the `featureflipper` directory to your Python path.

#. Add `featureflipper` to your `INSTALLED_APPS` setting.

#. Add `featureflipper.context_processors.features` to your TEMPLATE_CONTEXT_PROCESSORS setting.

#. Add `featureflipper.middleware.FeaturesMiddleware` to your MIDDLEWARE_CLASSES setting.


Limitations
===========

Feature status is currently kept in the database. This is
inefficient. They should probably be in Memcached instead.


What determines a feature's status
==================================

A feature's status (enabled or disabled) is determined by, in order:

#. The database: the value of the attribute `enabled` of the Feature
   table. You can edit this value using the Django admin application.

#. The session: if a session entry `feature_status_myfeature` exists,
   the feature will be enabled if the value is `enabled`, and disabled
   otherwise. The middleware will add this entry if the GET parameter
   session_enable_myfeature is included, as explained below.

#. The request: if a GET parameter `enabled_myfeature` exists, the
   feature will enabled for this request, as explained below.


Enabling and disabling features using URLs
==========================================

To enable a feature for the current request::

    /mypage/?enabled_myfeature

To enable a feature for this request and the rest of a session::

    /mypage/?session_enabled_myfeature

To clear all the features enabled in the session::

    /mypage/?session_clear_features


How to use the flippers in templates
====================================

The application registers itself with Django's admin app so you can
manage the `Features`. Each feature has a `name` made up of just
alphanumeric characters and hyphens that you can use in templates,
views, URLs and elsewhere in your code. Each feature has a Boolean
`enabled` property, which is False (disabled) by default. The app also
adds a few custom actions to the change list to help out. Features
also have a name and description, which aren't currently used anywhere
but are there to help you keep track of your features.

The context processor adds `features` to the template context, which
you can use like this::

    {% if feature.search %}
		  <form>...</form>
		{% endif %}

Here, `search` is the name of the feature. If the feature referenced
doesn't exist, it's treated as disabled. If you set the
TREAT_NONEXISTENT_FEATURES_AS_DISABLED configuration option to False,
Featureflipper will instead raise an exception (see above for
details).

To save you some typing, you can also use a new block tag::

		{% load feature_tag %}

		{% feature login %}
		  <a href="/login/">Login</a>
		{% endfeature %}

You can also do this::

		{% feature login %}
		  ... will only be output if the feature is enabled ...
    {% disabled %}
		  ... will only be output if the feature is disabled ...
		{% endfeature %}


How to use the flippers in views
================================

The middleware adds a `features` dictionary-like object to each request::

   if request.features['search']:
	   ...


Good practice
=============

- Once you no longer need to flip a feature, remove the feature from
  the database and all the logic from your template and views.

- If you decide to remove the feature itself from your application,
  don't leave unused template and view code around. Just delete it. If
  you later decide to resurect the feature, it'll always be there in
  your version control repository.

- Don't use features in the models. Keep everything in the templates
  and views. Your model needs to support both the enabled and disabled
  state of the feature. That's the point. You do the code push and any
  database migration, then control access to the feature in the
  view. For example, if you're changing your user profiles to allow
  several phone numbers rather than just the one, the model should
  allow multiple phone numbers. Users just won't be able to add (or
  see) those other phone numbers unless the feature is enabled for
  them.


TODOs and BUGS
==============

See: http://github.com/tobych/django-featureflipper/issues
