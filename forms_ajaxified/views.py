"""Views for the forms_ajaxified app."""
import json

from django.http import HttpResponse


class AjaxFormViewMixin(object):
    """Turns a FormView into a special view that can handle AJAX requests."""
    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({
                    'success': 0,
                    'trigger_element': self.request.REQUEST['trigger_element'],
                    'errors': form.errors,
                }), mimetype='application/json')
        return super(AjaxFormViewMixin, self).form_valid(form)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            return HttpResponse(
                json.dumps({
                    'success': 1,
                    'trigger_element': self.request.REQUEST['trigger_element'],
                }), mimetype='application/json')
        return super(AjaxFormViewMixin, self).form_valid(form)
