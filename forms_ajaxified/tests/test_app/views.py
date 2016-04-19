"""Dummy views for the tests of the forms_ajaxified app."""
from django.views.generic import (
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)
from django.views.generic.base import TemplateResponseMixin

from forms_ajaxified.views import AjaxDeleteViewMixin, AjaxFormViewMixin

from . import forms
from . import models


class DummyCreateView(TemplateResponseMixin, View):
    template_name = 'test_app/partials/dummy_form_wrapper.html'

    def post(self, request, *args, **kwargs):
        self.object = models.DummyModel.objects.create(title='Foo')
        self.form = forms.DummyForm(prefix=self.object.pk,
                                    instance=self.object)
        context = {'object': self.object, 'form': self.form, }
        return self.render_to_response(context, **kwargs)


class DummyDeleteView(AjaxDeleteViewMixin, DeleteView):
    model = models.DummyModel


class DummyTemplateView(TemplateView):
    template_name = 'test_app/dummy_template.html'

    def get_context_data(self):
        ctx = super(DummyTemplateView, self).get_context_data()
        ctx.update({'objects': models.DummyModel.objects.all(), })
        return ctx


class DummyFormView(AjaxFormViewMixin, FormView):
    form_class = forms.DummyForm
    template_name = 'test_app/partials/dummy_form.html'

    def get_success_url(self):
        return '/success/'


class DummyUpdateView(AjaxFormViewMixin, UpdateView):
    model = models.DummyModel
    fields = '__all__'
    template_name = 'test_app/partials/dummy_form.html'

    def dispatch(self, request, *args, **kwargs):
        # We don't want to deal with create views, only update views. If the
        # object doesn't exist already, we just create it.
        models.DummyModel.objects.get_or_create(pk=kwargs.get('pk'))
        return super(DummyUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(DummyUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs.update({'prefix': self.object.pk, })
        return form_kwargs

    def get_success_url(self):
        return '/success/'
