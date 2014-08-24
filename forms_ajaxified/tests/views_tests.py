"""Tests for the views of the forms_ajaxified app."""
import json

from django.test import RequestFactory, TestCase
from django.template.response import TemplateResponse

from .test_app import views


class AjaxFormViewMixinTestCase(TestCase):
    """Tests for the ``AjaxFormViewMixin`` class."""
    longMessage = True

    def test_dispatch(self):
        req = RequestFactory().get('/', data={'skip_form': 1, })
        result = views.DummyFormView().dispatch(req)
        self.assertEqual(result._headers['location'][1], '/success/', msg=(
            'When `skip_form` is in data, dispatch should just redirect to the'
            ' success URL.'))

        result = views.DummyUpdateView().dispatch(req, pk=1)
        self.assertEqual(result._headers['location'][1], '/success/', msg=(
            'When `skip_form` is in data, dispatch should just redirect to the'
            ' success URL.'))

    def test_form_invalid(self):
        req = RequestFactory().post(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data={'title': '1234', 'trigger_element': 'id_title'})
        resp = views.DummyFormView().dispatch(req)
        result = json.loads(resp.content)
        self.assertTrue('id_title' in result['errors'], msg=(
            'Should return a JSON dict which contains the form errors'))
        self.assertEqual(result['trigger_element'], 'id_title', msg=(
            'Should return the trigger element'))

        req = RequestFactory().post(
            '/', data={'title': '1234', 'trigger_element': 'id_title'})
        resp = views.DummyFormView().dispatch(req)
        self.assertTrue(isinstance(resp, TemplateResponse), msg=(
            'If called via non-ajax, it should return the partial template'))
