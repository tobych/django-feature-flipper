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

   This should work::

    pip install -e git+https://github.com/tobych/django-feature-flipper.git@master#egg=django-feature-flipper

#. Add `featureflipper` to your `INSTALLED_APPS` setting.

#. Add `featureflipper.context_processors.features` to your
   TEMPLATE_CONTEXT_PROCESSORS setting. It doesn't matter where you
   put it in relation to existing entries.

#. Add `featureflipper.middleware.FeaturesMiddleware` to your
   MIDDLEWARE_CLASSES setting. It doesn't matter where you put it in
   relation to existing entries.

#. Run ./manage.py syncdb to create the database table.


Good practice
=============

- Once you no longer need to flip a feature, remove the feature from
  the database and all the logic from your template and views.

- If you decide to remove the feature itself from your application,
  don't leave unused template and view code around. Just delete it. If
  you later decide to resurect the feature, it'll always be there in
  your version control repository.

- Don't query feature states in the models. Keep everything in the
  templates and views. Your model needs to support both the enabled
  and disabled state of the feature. That's the point. You do the code
  push and any database migration, then control access to the feature
  in the view. For example, if you're changing your user profiles to
  allow several phone numbers rather than just the one, the model
  should allow multiple phone numbers. Users just won't be able to add
  (or see) those other phone numbers unless the feature is enabled for
  them.


TODOs and BUGS
==============

See: https://github.com/tobych/django-feature-flipper/issues
