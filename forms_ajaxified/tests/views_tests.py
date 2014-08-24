"""Tests for the views of the forms_ajaxified app."""
from django.test import RequestFactory, TestCase

from .test_app.views import DummyFormView


class AjaxFormViewMixinTestCase(TestCase):
    """Tests for the ``AjaxFormViewMixin`` class."""
    longMessage = True

    def test_dispatch(self):
        req = RequestFactory().get('/', data={'skip_form': 1, })
        result = DummyFormView().dispatch(req)
        self.assertEqual(result._headers['location'][1], '/success/', msg=(
            'When `skip_form` is in data, dispatch should just redirect to the'
            ' success URL.'))
