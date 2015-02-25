"""Views for the forms_ajaxified app."""
import json

from django.http import HttpResponse
from django.shortcuts import redirect


class AjaxDeleteViewMixin(object):
    """Turns any view into a delete view for a given ContentType and PK."""
    def post(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        try:
            obj = self.get_object()
            obj.delete()
            return HttpResponse(
                json.dumps({'success': 1, }),
                mimetype='application/json')
        except Exception, ex:
            return HttpResponse(
                json.dumps({'error': ex.message, }),
                mimetype='application/json')


class AjaxFormViewMixin(object):
    """Turns a FormView into a special view that can handle AJAX requests."""
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        if 'skip_form' in request.REQUEST:
            self.kwargs = kwargs
            if hasattr(self, 'get_object'):
                self.object = self.get_object()
            return redirect(self.get_success_url())
        return super(AjaxFormViewMixin, self).dispatch(
            request, *args, **kwargs)

    def form_invalid(self, form):
        if self.request.is_ajax():
            errors = {}
            for field_name, field_errors in form.errors.items():
                field = 'id_'
                if form.prefix:
                    field += str(form.prefix)
                    field += '-'
                field += field_name
                errors[field] = field_errors.as_ul()
            return HttpResponse(
                json.dumps({
                    'success': 0,
                    'trigger_element': self.request.REQUEST.get(
                        'trigger_element', ''),
                    'errors': errors,
                }), mimetype='application/json')
        return super(AjaxFormViewMixin, self).form_invalid(form)

    def form_valid(self, form, form_valid_redirect=None):
        """
        Returns JSON success response or redirects to success URL.

        :param form_valid_redirect: When you leave this as ``None``, the mixin
          tries to get the value from the POST or GET data. If you set this
          to ``True`` or ``False``, it will override eventually set POST or
          GET data for the key ``form_valid_redirect``.

        """
        self.object = form.save()
        if form_valid_redirect is None:
            form_valid_redirect = self.request.POST.get(
                'form_valid_redirect', None)
        if form_valid_redirect is None:
            form_valid_redirect = self.request.GET.get(
                'form_valid_redirect', None)
        if self.request.is_ajax() and not form_valid_redirect:
            return HttpResponse(
                json.dumps({
                    'success': 1,
                    'trigger_element': self.request.REQUEST.get(
                        'trigger_element'),
                }), mimetype='application/json')
        return super(AjaxFormViewMixin, self).form_valid(form)
