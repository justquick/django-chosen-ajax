import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Pony


class MetaDataViewsTest(TestCase):

    def setUp(self):
        """
        Create some ponies to be used in tests.
        """
        ponies = [
            {'name': 'Star', 'breed': 'quarter horse'},
            {'name': 'Dakota', 'breed': 'quarter horse'},
            {'name': 'Cheyenne', 'breed': 'thoroughbred'},
            {'name': 'Misty', 'breed': 'thoroughbred'},
        ]
        for obj in ponies:
            p = Pony.objects.create(**obj)


    def test_ajax_view(self):
        """
        Test that the view works properly.
        """
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('chosen_lookup')
        get_data = {'q': 'horse', 'model': 'pony', 'app': 'chosen', 'fields': 'name breed'}
        response = self.client.get(url, get_data, **kwargs)
        print response.content
        self.assertEqual(response.status_code, 200)

        json_string = response.content
        data = json.loads(json_string)  
        self.assertEqual(data[0]['text'], u'')
        self.assertEqual(data[1]['text'], u'')

