from django.db.models import get_model
from django.forms.util import flatatt
from django.forms.widgets import Select, SelectMultiple
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class ChosenSelect(Select):

    def __init__(self, attrs=None, *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'chznSelect expanded'
        attrs['data-placeholder'] = 'Select an option...'
        super(ChosenSelect, self).__init__(attrs, *args, **kwargs)


class ChosenSelectMultiple(SelectMultiple):

    def __init__(self, attrs=None, *args, **kwargs):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'chznSelect expanded'
        attrs['multiple'] = 'multiple'
        attrs['data-placeholder'] = 'Select an option...'
        super(ChosenSelectMultiple, self).__init__(attrs, *args, **kwargs)


class ChosenAjax(SelectMultiple):

    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        super(ChosenAjax, self).__init__(attrs, choices)
        self.attrs.update({
            'class': 'chznAjax expanded',
            'multiple': 'multiple',
            'data-placeholder': 'Type to search...',
        })

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        for obj in get_model(self.attrs['data-app'], self.attrs['data-model']).objects.filter(pk__in=value):
            output.append(self.render_option(obj.pk, obj))
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = u' selected="selected"'
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))
