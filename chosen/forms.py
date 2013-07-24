from django import forms
from django.db import models
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from . import widgets


class ChosenAdminForm(forms.ModelForm):

    class Media:
        css = {
            'all': ('css/main.css', 'css/chosen.css', )
        }
        js = (
            'js/chosen.min.js',
            'js/chosen.ajax.js', 
            'js/main.js',
        )

    def __init__(self, *args, **kwargs):
        super(ChosenAdminForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].__class__.__name__ in ['ChoiceField', 'TypedChoiceField', 'MultipleChoiceField']:
                self.fields[field].widget = widgets.ChosenSelect(choices=self.fields[field].choices) 
            elif self.fields[field].__class__.__name__ in 'ModelChoiceField':
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelect(choices=self.fields[field].choices), self.instance._meta.get_field(field).rel, self.admin_site)
            elif self.fields[field].__class__.__name__ is 'ModelMultipleChoiceField':
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelectMultiple(choices=self.fields[field].choices), self.instance._meta.get_field(field).rel, self.admin_site)
            elif self.fields[field].__class__.__name__ is 'ChosenAjaxField':
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenAjax(choices=self.fields[field].choices), self.instance._meta.get_field(field).rel, self.admin_site)
                # Set attrs onto the widget so that we can pass it to the view for the queryset.
                self.fields[field].widget.attrs['data-model'] = self.fields[field].queryset.model._meta.module_name
                self.fields[field].widget.attrs['data-app'] = self.fields[field].queryset.model._meta.app_label
                self.fields[field].widget.attrs['data-fields'] = self.fields[field].search_fields

    def clean(self):
        """Custom clean method to strip whitespaces from CharField and TextField."""
        cleaned_data = super(ChosenAdminForm, self).clean()
        for field in cleaned_data:
            if isinstance(self.instance._meta.get_field(field), (models.CharField, models.TextField)):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data
