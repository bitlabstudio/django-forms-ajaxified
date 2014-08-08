Django Forms Ajaxified
============

A reusable Django app that allows to submit forms via AJAX.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-forms-ajaxified

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-forms-ajaxified.git#egg=forms_ajaxified

TODO: Describe further installation steps (edit / remove the examples below):

Add ``forms_ajaxified`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'forms_ajaxified',
    )

Add the ``forms_ajaxified`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^forms-ajaxified/', include('forms_ajaxified.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load forms_ajaxified_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate forms_ajaxified


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-forms-ajaxified
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
