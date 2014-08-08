"""Dummy URLs for the tests of the forms_ajaxified app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'$',
        views.DummyTemplateView.as_view(),
        name='dummy_template_view'),
    url(r'dummy-form/$',
        views.DummyFormView.as_view(),
        name='dummy_form_view'),
)
