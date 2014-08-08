"""Dummy views for the tests of the forms_ajaxified app."""
from django.views.generic import FormView, TemplateView

from . import forms


class DummyTemplateView(TemplateView):
    template_name = 'test_app/dummy_template.html'


class DummyFormView(FormView):
    form_class = forms.DummyForm
    template_name = 'test_app/partials/dummy_form.html'
