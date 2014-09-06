"""Dummy URLs for the tests of the forms_ajaxified app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'dummy-form/create/$',
        views.DummyCreateView.as_view(),
        name='dummy_create_view'),
    url(r'dummy-form/delete/(?P<pk>\d+)/$',
        views.DummyDeleteView.as_view(),
        name='dummy_delete_view'),
    url(r'dummy-form/(?P<pk>\d+)/$',
        views.DummyUpdateView.as_view(),
        name='dummy_form_view'),
    url(r'$',
        views.DummyTemplateView.as_view(),
        name='dummy_template_view'),
)
