"""Dummy models for the tests of the forms_ajaxified app."""
from django.db import models


class DummyModel(models.Model):
    """Dummy model for the tests of the forms_ajaxified app."""
    title = models.CharField(max_length=256, null=True)
    short_description = models.CharField(max_length=512, null=True, blank=True)
