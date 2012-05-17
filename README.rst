==============
django-icanhaz
==============

A templatetag for easier integration of `ICanHaz.js`_ JavaScript templates with
Django templates.

.. _ICanHaz.js: http://icanhazjs.com

Quickstart
==========

Dependencies
------------

Tested with `Django`_ 1.3 through trunk, and `Python`_ 2.6 and 2.7. Almost
certainly works with older versions of both.

.. _Django: http://www.djangoproject.com/
.. _Python: http://www.python.org/

Installation
------------

Install from PyPI with ``pip``::

    pip install django-icanhaz

or get the `in-development version`_::

    pip install django-icanhaz==dev

.. _in-development version: https://github.com/carljm/django-icanhaz/tarball/master#egg=django_secure-dev

Usage
-----

* Add ``"icanhaz"`` to your ``INSTALLED_APPS`` setting.

* Set the ``ICANHAZ_DIRS`` setting to a list of full (absolute) path to
  directories where you will store your ICanHaz templates.

* ``{% load icanhaz %}`` and use ``{% icanhaz "templatename" %}`` in your
  Django templates to safely embed the ICanHaz.js template at
  ``<ICANHAZ_DIRS-entry>/templatename.html`` into your Django template,
  automatically wrapped in ``<script id="templatename" type="text/html">``,
  ready for ``ich.templatename({...})`` in your JavaScript.

``django-icanhaz`` does not bundle `ICanHaz.js`_ or provide any JavaScript
utilities; it just helps you easily embed the templates in your HTML. Include
`ICanHaz.js`_ in your project's static assets and use it in your JS as usual.


Regular Expressions in Template Tags
------------------------------------

Using the template tag ``{% icanhaz [directory] [regex] %}`` in your
Django templates will embed all files matching that regex in the given
directory.  So, ``{% icanhaz './' '.*_template' %}`` would match
`note_template.html` and `comment_template.html`, giving them templatename
`note_template` and `comment_template`, respectively.  (Note that the ".html"
extension is assumed.  See the advanced usage section for how to customize
this behavior).


Advanced usage
--------------

You can also bundle ICanHaz templates with Django reusable apps; by default
``django-icanhaz`` will look for templates in a ``jstemplates`` subdirectory of
each app in ``INSTALLED_APPS``. The app subdirectory name(s) to check can be
configured via the ``ICANHAZ_APP_DIRNAMES`` setting, which defaults to
``["jstemplates"]``.

Standard finding of templates can be fully controlled via the ``ICANHAZ_FINDERS``
setting, which is a list of dotted paths to finder classes. A finder class
should be instantiable with no arguments, and have a ``find(name)`` method
which returns the full absolute path to a template file, given a base-name.

Regex finding of templates can be fully controlled via the
``ICANHAZ_REGEX_FINDERS`` setting.  A regex finder class should be
instantiable with no arguments and have a ``find(dir, regex)`` method
which takes in two strings (directory and regex) and returns a list of
matches in the form `[(name, filepath)...]` where name is the id given
to a template and filepath is a full absolute path to a template file.

By default, ``ICANHAZ_FINDERS`` contains ``"icanhaz.finders.FilesystemFinder"``
(which searches directories listed in ``ICANHAZ_DIRS``) and
``"icanhaz.finders.AppFinder"`` (which searches subdirectories named in
``ICANHAZ_APP_DIRNAMES`` of each app in ``INSTALLED_APPS``), in that order --
thus templates found in ``ICANHAZ_DIRS`` take precedence over templates in
apps.

By default, ``ICANHAZ_REGEX_FINDERS`` contains
``"icanhaz.finders.FilesystemRegexFinder"` (which searches directories listed
in ``ICANHAZ_DIRS``) and ``"icanhaz.finders.AppRegexFinder"`` (which searches
subdirectories named in ``ICANHAZ_APP_DIRNAMES`` of each app in
``INSTALLED_APPS``).  Precedence is unimportant, as all matching templates
are added.  Further, django-icanhaz is bundled with two convenience scoping
regex finders: ``icanhaz.finders.ScopedFilesystemRegexFinder`` and
``icanhaz.finders.ScopedAppRegexFinder`` which each prepend a scope derived
from the directory path given to each name: so, if
``{% icanhaz './all/my/templates/' '.*_template' %}`` matches
`note_template.html` and `comment_template.html`, they will have names
`all_my_templates_note_template` and `all_my_templates_comment_template`,
respectively.


Rationale
---------

The collision between Django templates' use of ``{{`` and ``}}`` as template
variable markers and `ICanHaz.js`_' use of same has spawned a variety of
solutions. `One solution`_ simply replaces ``[[`` and ``]]`` with ``{{`` and
``}}`` inside an ``icanhaz`` template tag; `another`_ makes a valiant attempt
to reconstruct verbatim text within a chunk of a Django template after it has
already been mangled by the Django template tokenizer.

I prefer to keep my JavaScript templates in separate files in a dedicated
directory anyway, to avoid confusion between server-side and client-side
templating. So my contribution to the array of solutions is essentially just an
"include" tag that avoids parsing the included file as a Django template (and
for convenience, automatically wraps it in the script tag that `ICanHaz.js`_
expects to find it in).

Enjoy!

.. _one solution: https://gist.github.com/975505
.. _another: https://gist.github.com/629508
