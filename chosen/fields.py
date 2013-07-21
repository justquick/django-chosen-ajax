from django.forms.models import ModelMultipleChoiceField


class ChosenAjaxField(ModelMultipleChoiceField):

    def __init__(self, queryset, search_fields=None, *args, **kwargs):
        super(ChosenAjaxField, self).__init__(queryset, search_fields, *args, **kwargs)
        self.search_fields = ' '.join([value for value in search_fields]) if search_fields else None

