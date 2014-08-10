"""Dummy views for the tests of the forms_ajaxified app."""
from django.views.generic import TemplateView

from forms_ajaxified.views import AjaxFormView

from . import forms
from . import models


class DummyTemplateView(TemplateView):
    template_name = 'test_app/dummy_template.html'


class DummyFormView(AjaxFormView):
    form_class = forms.DummyForm
    template_name = 'test_app/partials/dummy_form.html'

    def dispatch(self, request, *args, **kwargs):
        # We don't want to deal with create views, only update views. If the
        # object doesn't exist already, we just create it.
        models.DummyModel.objects.get_or_create(pk=kwargs.get('pk'))
        return super(DummyFormView, self).dispatch(request, *args, **kwargs)
