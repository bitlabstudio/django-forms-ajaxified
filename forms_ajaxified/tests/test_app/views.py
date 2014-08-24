"""Dummy views for the tests of the forms_ajaxified app."""
from django.views.generic import FormView, TemplateView, UpdateView

from forms_ajaxified.views import AjaxFormViewMixin

from . import forms
from . import models


class DummyTemplateView(TemplateView):
    template_name = 'test_app/dummy_template.html'


class DummyFormView(AjaxFormViewMixin, FormView):
    form_class = forms.DummyForm
    template_name = 'test_app/partials/dummy_form.html'

    def get_success_url(self):
        return '/success/'


class DummyUpdateView(AjaxFormViewMixin, UpdateView):
    model = models.DummyModel
    template_name = 'text_app/partials/dummy_form.html'

    def dispatch(self, request, *args, **kwargs):
        # We don't want to deal with create views, only update views. If the
        # object doesn't exist already, we just create it.
        models.DummyModel.objects.get_or_create(pk=kwargs.get('pk'))
        return super(DummyUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/success/'
