import json
import operator

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from django.views.generic import View


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        try:
            return json.dumps(context)
        except:
            pass


class ChosenLookup(JSONResponseMixin, View):
   
    def get(self, request, *args, **kwargs):
        """
        Ajax-only view that parses a querystring for the search term, the model name, and the search fields
        to build a queryset with. Returns a json response in the format for value, text.
        """
        if request.is_ajax():
            app = request.GET.get('app', None)
            term = request.GET.get('q', None)
            model = request.GET.get('model', None)
            fields = request.GET.get('fields', None)
            if term and model and fields and app:
                try:
                    ct = ContentType.objects.get(app_label=app, model=model)
                except ContentType.DoesNotExist:
                    raise http404
                ct_class = ct.model_class()
                conditions =[]
                for field in fields.split():
                    conditions.append({
                        '{}__icontains'.format(field): term
                    })
                lookups = []
                for obj in conditions:
                    lookups.append(Q(**obj))
                qs = ct_class.objects.filter(reduce(operator.or_, lookups))
                context = [{'value': item.pk, 'text': unicode(item)} for item in qs]
                return self.render_to_json_response(context, *args, **kwargs)
        raise Http404


