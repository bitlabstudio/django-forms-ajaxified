"""Dummy views for the tests of the forms_ajaxified app."""
from django.views.generic import FormView, TemplateView

from . import forms
from . import models


class DummyTemplateView(TemplateView):
    template_name = 'test_app/dummy_template.html'


class DummyFormView(FormView):
    form_class = forms.DummyForm
    template_name = 'test_app/partials/dummy_form.html'

    def dispatch(self, request, *args, **kwargs):
        # We don't want to deal with create views, only update views. If the
        # object doesn't exist already, we just create it.
        models.DummyModel.get_or_create(pk=kwargs.get('pk'))
        return super(DummyFormView, self).dispatch(request, *args, **kwargs)
