from django import forms
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
        # Here we cycle through the fields and set the field to use the Chosen library widgets.
        # NOTE: We get and then set the queryset in ModelChoice and ModelMulptipleChoiceField because using the
        # RelatedFieldWidgetWrapper clears out the queryset for some reason. 
        for field in self.fields:
            if self.fields[field].__class__.__name__ in ['ChoiceField', 'TypedChoiceField', 'MultipleChoiceField']:
                choices = self.fields[field].choices
                self.fields[field].widget = widgets.ChosenSelect(choices=choices) 
            elif self.fields[field].__class__.__name__ in 'ModelChoiceField':
                queryset = self.fields[field].queryset
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelect(), self.instance._meta.get_field(field).rel, self.admin_site)
                self.fields[field].queryset = queryset 
            elif self.fields[field].__class__.__name__ is 'ModelMultipleChoiceField':
                queryset = self.fields[field].queryset
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenSelectMultiple(), self.instance._meta.get_field(field).rel, self.admin_site)
                self.fields[field].queryset = queryset 
            elif self.fields[field].__class__.__name__ is 'ChosenAjaxField':
                queryset = self.fields[field].queryset
                self.fields[field].widget = RelatedFieldWidgetWrapper(
                    widgets.ChosenAjax(), self.instance._meta.get_field(field).rel, self.admin_site)
                self.fields[field].queryset = queryset 
                # Set attrs onto the widget so that we can pass it to the view for the queryset.
                self.fields[field].widget.attrs['data-model'] = self.fields[field].queryset.model._meta.module_name
                self.fields[field].widget.attrs['data-app'] = self.fields[field].queryset.model._meta.app_label
                self.fields[field].widget.attrs['data-fields'] = self.fields[field].search_fields

    def clean(self):
        """Custom clean method to strip whitespaces from CharField and TextField."""
        cleaned_data = super(ChosenAdminForm, self).clean()
        for field in cleaned_data:
            if self.instance._meta.get_field(field).__class__.__name__ in ('CharField', 'TextField',):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data
