"""Templatetags for the forms_ajaxified app."""
from django import template
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.assignment_tag
def get_contenttype_pk(obj):
    """Returns the contenttype for the given object"""
    return ContentType.objects.get_for_model(obj).pk
