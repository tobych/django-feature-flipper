======================
Django Feature Flipper
======================

django-feature-flipper allows you to flip features of your Django site
on and off, so you can deploy code and schema changes for upcoming
features but hide the features from your users until you're ready.

This practice is commonly used in continuous deployment.

The term "feature flipper" seems to have come from Flickr, as
described in this often-cited blog post:

http://code.flickr.com/blog/2009/12/02/flipping-out/

Feature flags or switches are becoming more commonly used, it seems.

django-feature-flipper is in part inspired by that post, along with
some of the other feature flippers available, including:

- https://github.com/qype/feature_flipper (for Rails, by Florian Munz at Qype)
- https://github.com/grillpanda/dolphin (for Rails, by Matt Johnson)
- http://dhorrigan.com/turnstiles/ (for CodeIgniter, Dan Horrigan)
- https://dev.launchpad.net/LEP/FeatureFlags (for Canonical's Launchpad)

A few days after I first committed django-feature-flipper to github,
David Cramer at Disqus has released the "gargoyle" plugin for Django,
that offers overlapping functionality. That plugin requires "Nexus",
their Django front-end admin replacement.

- http://justcramer.com/2010/12/21/feature-switches-in-django-with-gargoyle/
- https://github.com/disqus/gargoyle

The following post is an interview with Flickr's John Allspaw, author
of "The Art of Capacity Planning: Scaling Web Resources."

- http://highscalability.com/blog/2009/6/29/how-to-succeed-at-capacity-planning-without-really-trying-an.html

Includes this quote, which covers feature flags being used to
**disable** features to help "panic gracefully.":

"Of course it's easier to do those things when you have easy config
flags to turn things on or off, and a list to run through of what
things are acceptable to serve stale and static. We currently have
about 195 'features' we can turn off at Flickr in dire
circumstances. And we've used those flags when we needed to."

More on feature flags/flippers:

- http://old.nabble.com/Feature-Flipper-to30400696.html 
- http://www.alandelevie.com/2010/05/19/feature-flippers-with-rails/
- http://engineering.qype.com/2010/06/03/how-we-work-flipping-features/ (also Florian Munz)
- http://www.reddit.com/r/programming/comments/aehta/flickr_dont_branch/

Continuous deployment:

- http://www.startuplessonslearned.com/2009/06/why-continuous-deployment.html
- http://timothyfitz.wordpress.com/2009/02/10/continuous-deployment-at-imvu-doing-the-impossible-fifty-times-a-day/
- http://radar.oreilly.com/2009/03/continuous-deployment-5-eas.html
- http://en.wikipedia.org/wiki/Lean_Startup


Installation
============

#. Add the ``featureflipper`` directory to your Python path.

   This should work::

    pip install -e git+https://github.com/tobych/django-feature-flipper.git@master#egg=django-feature-flipper

#. Add ``featureflipper`` to your ``INSTALLED_APPS`` setting.

#. Add ``featureflipper.context_processors.features`` to your
   ``TEMPLATE_CONTEXT_PROCESSORS`` setting. It doesn't matter where
   you put it in relation to existing entries.

#. Add ``featureflipper.middleware.FeaturesMiddleware`` to your
   ``MIDDLEWARE_CLASSES`` setting. It doesn't matter where you put it
   in relation to existing entries.

#. Optionally, add a settings.FEATURES_FILE, and set it to the
   location of a features file (see below) to load after each syncdb
   (or whenever you'd normally expect fixtures to be loaded).

#. Run ``./manage.py syncdb`` to create the database table.


Limitations
===========

Feature status is currently kept in the database. This is
inefficient. They should probably be in Memcached instead.

There is, unforgivably, poor unit test coverage.


What determines a feature's status
==================================

A feature's status (enabled or disabled) is determined by, in order:

#. The database: the value of the attribute ``enabled`` of the
   ``Feature`` table. You can edit this value using the Django admin
   application.

#. The session: if a session entry ``feature_status_myfeature``
   exists, the feature will be enabled if the value is ``enabled``,
   and disabled otherwise. The middleware will add this entry if the
   ``GET`` parameter ``session_enable_myfeature`` is included, as
   explained below.

#. The request: if a GET parameter ``enabled_myfeature`` exists, the
   feature will enabled for this request, as explained below.


Enabling and disabling features using URLs
==========================================

Users with permission ``can_flip_with_url`` can turn features on and
off using URL parameters.

To enable a feature for the current request::

  /mypage/?enable_myfeature

To enable a feature for this request and the rest of a session::

  /mypage/?session_enable_myfeature

To clear all the features enabled in the session::

  /mypage/?session_clear_features

If you want to allow anonymous users to do this, see the section
"Authorization for Anonymous Users" here:

http://docs.djangoproject.com/en/dev/topics/auth/

Alternatively (since that looks painful) you can allow anyone to use
URLs to flip features by setting
FEATURE_FLIPPER_ANONYMOUS_URL_FLIPPING to True in your settings.py.


How to use the features in templates
====================================

The application registers itself with Django's admin app so you can
manage the ``Features``. Each feature has a ``name`` made up of just
alphanumeric characters and hyphens that you can use in templates,
views, URLs and elsewhere in your code. Each feature has a boolean
``enabled`` property, which is ``False`` (disabled) by default. The
app also adds a few custom actions to the change list page so you can
enable, disable and flip features there.

Features also have a name and description, which aren't currently used
anywhere but should help you keep track.

The context processor adds ``features`` to the template context, which
you can use like this::

  {% if feature.search %}
    <form>...</form>
  {% endif %}

Here, ``search`` is the name of the feature. If the feature referenced
doesn't exist, it is silently treated as disabled.

To save you some typing, you can also use a new block tag::

  {% load feature_tag %}

  {% feature login %}
    <a href="/login/">Login</a>
  {% endfeature %}

You can also do this::

  {% feature profile %}
    ... will only be output if feature 'profile' is enabled ...
  {% disabled %}
    ... will only be output if the feature is disabled ...
  {% endfeature %}


How to use the features in views
================================

The middleware adds ``features``, a dict subclass, to each request::

  if request.features['search']:
	 ...

The middleware also adds ``features_panel`` to the request. This
object provides more information about the state of each feature than
``features``.

``enabled('myfeature')`` returns True if myfeature is enabled.

``source('myfeature')`` returns a string indicating the source of the
final status of the feature:

- ``site``: site-wide, in the Feature instance itself
- ``session``: in the session, set using a URL parameter
- ``url``: per request, set using a URL parameter

``source('myfeature)`` will return another value if a featureflipper
plugin is being used (see below).


Features file
=============

To make sure you can easily keep features and their default settings
under version control, you can load features from a file using the
``loadfeatures`` management command (below). If you add FEATURES_FILE
to your settings, pointing to a file (typically features.json),
features from this file will be loaded each time you do a syncdb. Note
that any existing feature of the same name will be overwritten.

The file needs to look like this::

  [
    {
      "name": "profile",
      "enabled": true,
      "description": "Allow the user to view and edit their profile."
    },
    {
      "name": "search",
      "enabled": true,
      "description": "Shows the search box on most pages, and the larger one on the home page."
    }
  ]

Note that for ``profile`` above, we're using the ``description`` field
to describe the feature in general, whereas for ``search`` we're
describing how and where that feature is make visible to the user. You
might end up using a mix of these.


Management commands
===================

- ``./manage.py features``: List the features in the database, along
  with their status.

- ``./manage.py addfeature``: Adds one or more features to the
  database (leaving them disabled).

- ``./manage.py loadfeatures``: Loads features from a JSON file (as
  above), or from the features file defined in settings.FEATURES_FILE.

- ``./manage.py dumpfeatures``: Outputs features from the database in
  the same JSON format (although the keys aren't in the same order as the
  example above).

- ``./manage.py enablefeature``: Enables the named feature(s).

- ``./manage.py disablefeature``: Disables the named feature(s).


Signals
=======

Signal featureflipper.signals.feature_defaulted is sent when a feature
referred to in a template or view is being defaulted to disabled. This
will happen if the feature is not in the database, and hasn't been
enabled using URL parameters.

The example project shows how this signal can be used, in ``views.py``.

Note also that featureflipper uses Django's ``post_syncdb`` to load a
features file when ``syncdb`` is run. The connection to the signal is
made in ``featureflipper/management/__init.py__``.


Using the example project included in the source
================================================

The source tree for django-feature-flipper includes an example project
created using the "App Factory" described on a post_ on the Washington
Times open source blog.

.. _post: http://opensource.washingtontimes.com/blog/2010/nov/28/app-centric-django-development-part-2-app-factory/

The settings.py file stipulates a sqlite3 database, so you'll need
sqlite3 to be installed on your system. The database will be created
automatically as necessary.

To try the example project::

 cd example
 ./manage.py syncdb
 ./manage.py runserver

Let syncdb help you create a superuser so you can use the admin to
create your own features. If you forget this step you can always run
the ``createsuperuser`` command to do this. Two features (``profile``
and ``search``) will be loaded from ``features.json`` when you do the
``syncdb``. These are referenced in the example template used on the
home page. There's no link bank to the home page from the admin so
you'll need to hack the URL or open the admin in a separate tab in
your browser.


Good practice
=============

- Once you no longer need to flip a feature, remove the feature from
  the database and all the logic from your template and views.

- If you decide to remove the feature itself from your application,
  don't leave unused template and view code around. Just delete it. If
  you later decide to resurect the feature, it'll always be there in
  your version control repository.


Extending Feature Flipper
=========================

The app includes a hook to allow you to add "feature providers" that
provide the state of features. On each request, the feature states are
collected in turn from any plugins found (the order they're called on
is undefined), just after feature states are collected from the
database. To add a plugin, you need to create a subclass of
featureflipper.FeatureProvider, and make sure it gets compiled along
with the rest of your application.

The class attribute ``source`` must be a string. This string is what
the middeware makes available in request.features_panel.source().

The static method ``features`` must return a (possibly empty) list of
tuples. The first member is the name of the feature, and the second
True if the feature is enabled, and False otherwise. The features
returned need not be defined in a Feature instance in the database.

For example::

  from featureflipper import FeatureProvider
  class UserFeatures(FeatureProvider):
    source = 'user'
    @staticmethod
    def features(request):
      return [('feature1', False), ('feature2', True)]


TODOs and BUGS
==============

See: https://github.com/tobych/django-feature-flipper/issues
