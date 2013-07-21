from itertools import chain

from django.forms.util import flatatt
from django.forms.widgets import Select, SelectMultiple
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text, force_unicode
from django.utils.safestring import mark_safe


class ChosenSelect(Select):

    def __init__(self, attrs={}, *args, **kwargs):
        attrs['class'] = 'chznSelect expanded'
        attrs['data-placeholder'] = 'Select an option...'
        super(ChosenSelect, self).__init__(attrs, *args, **kwargs)


class ChosenSelectMultiple(SelectMultiple):

    def __init__(self, attrs={}, *args, **kwargs):
        attrs['class'] = 'chznSelect expanded'
        attrs['multiple'] = 'multiple'
        attrs['data-placeholder'] = 'Select an option...'
        super(ChosenSelectMultiple, self).__init__(attrs, *args, **kwargs)


class ChosenAjax(SelectMultiple):

    def __init__(self, attrs={}, choices=(), *args, **kwargs):
        attrs['class'] = 'chznAjax expanded'
        attrs['multiple'] = 'multiple'
        attrs['data-placeholder'] = 'Type to search...'
        super(ChosenAjax, self).__init__(attrs, *args, **kwargs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if force_unicode(option_value) in selected_choices:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output) 

