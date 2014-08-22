Django Forms Ajaxified
======================

A reusable Django app that allows to submit forms via AJAX.

**This is useful for two usecases:i**

1. You have a very long form and you want to signal to your users that each
   field they fill out is saved immediately and you want to show validation
   errors immediately.
2. You have a number of different forms that all have their own small
   AJAX-views and partial templates and you all include them in one bigger
   template. Each form should be able to communicate with it's own AJAX-view
   independently.

**Features:**

1. Error messages are displayed next to the field, when they happen
2. A visual indicator is displayed on the field that has just been changed to
   indicate that this value has been saved.


Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-forms-ajaxified

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-forms-ajaxified.git#egg=forms_ajaxified

Add ``forms_ajaxified`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'forms_ajaxified',
    )

In your ``base.html`` include the jQuery plugin that loads your forms and
handles the AJAX responses. You should place it somewhere below your jQuery
include:

.. code-block:: html

    {% load static %}
    ...
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="{% static "forms_ajaxified/js/forms_ajaxified.js" %}></script>

At the bottom of your ``base.html`` or whereever you run global
initialisations, activate the jQuery plugin:

.. code-block:: html

    <script>
        $(document).ready(function() {
            $('[data-class="form_ajaxified"]').formsAjaxified();
        });
    </script>

If you are using Bootstrap, you can add a green border around an input element
via CSS transitions similar to the blue border when the element is focused.
Simply add the following to your project's styles:

.. code-block:: less

    input.success, textarea.success, select.success {
        @color-rgba: rgba(red(@brand-success), green(@brand-success), blue(@brand-success), .6);
        border-color: @color-rgba;
        .box-shadow(~"inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px @{color-rgba}");
    }

Usage
-----

This example assumes that you have a big ``TemplateView`` that contains one
or more small partial templates with forms. You could just as well just use
one big ``FormView``, as usual.

First you should write a TemplateView that renders the whole template and
reserves some space for its one or many forms to be loaded:

.. code-block:: python

    from django.views.generic import TemplateView

    class MyTemplateView(TemplateView):
        template_name = 'myapp/my_template_view.html'

The template for this view should look something like this:

.. code-block:: html

    {% extends "base.html" %}
    <form method="post" action="{% url "my_form_view" %}" data-class="form_ajaxified"></form>

As you can see, the form is empty but thanks to the ``data-class`` attribute,
our jQuery plugin will be able to find all such forms on your template. It will
read the ``action`` attribute and send an AJAX GET request to the ``action``
view and initially retrieve the returned partial.

Now you should write a simple Form and a FormView that returns the partial
template that renders this form. By adding the ``AjaxFormViewMixin`` you
enable your view to return proper JSON responses when handling POST requests.
We only show a code snippet for one such FormView but you could have many of
them and load them all in a TemplateView that ties everything together:

.. code-block:: python

    from django.views.generic import FormView
    from forms_ajaxified.views import AjaxFormViewMixin
    from myapp.forms import MyForm

    class MyFormView(AjaxFormViewMixin, FormView):
        form_class = MyForm
        template_name = 'myapp/partials/my_form.html'

The partial template for your form should look something like below. Note that
the template does not contain a ``form`` tag because we already have that in
the "outer" template of the TemplateView above:

.. code-block:: html

    {% for field in form %}
        {% include "django_libs/partials/forms/form_field.html" %}
    {% endfor %}
    <input type="submit" name="btn_submit" value="Submit" />

If everything is setup correctly, the jQuery plugin will initially load all
forms and then monitor all changes in their fields. On every data change, it
will send a POST request to the corresponding AJAX-view. If validation errors
happen, they will appear next to their fields. If data was saved successfully,
a visual indicator will inform the user about this. In theory, the form would
not even need a submit button, it is up to the developer to decide if it should
be there or not.

jQuery Plugin Options
---------------------

The jQuery plugin supports the following options:

default_loading_text
++++++++++++++++++++

Default: `Submitting...`

Set this if you want to use a different text to be shown on submit buttons when
submitting the form. The original button text will be replaced with this one
and the button will be disabled. When the request returns, the changes will
be undone.

jQuery Plugin Data Attributes
-----------------------------

The following data attributes allow to adjust the behaviour of the plugin:

data-id="form_ajaxified"
++++++++++++++++++++++++

Set this attribute on all forms that should be controlled by this app.

data-loading-text="Loading..."
++++++++++++++++++++++++++++++

Set this attribute on submit buttons that should have special loading texts.
This overrides the plugin option `default_loading_text`.

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
