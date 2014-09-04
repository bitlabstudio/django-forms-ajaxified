"""Tests for the templatetags of the forms_ajaxified app."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..templatetags import forms_ajaxified_tags as tags
from .test_app.models import DummyModel


class GetContenttypePkTestCase(TestCase):
    """Tests for the ``get_contenttype_pk`` assignment tag."""
    longMessage = True

    def test_tag(self):
        obj = DummyModel.objects.create()
        ctype = ContentType.objects.get_for_model(obj)
        result = tags.get_contenttype_pk(obj)
        self.assertEqual(result, ctype.pk, msg=(
            'Should return the PK of the ContentType instance that belongs to'
            ' the given object'))
