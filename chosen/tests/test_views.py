import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Pony


class MetaDataViewsTest(TestCase):

    def setUp(self):
        """
        Create some ponies to be used in tests, create test User.
        """
        ponies = [
            {'name': 'Star', 'breed': 'quarter horse'},
            {'name': 'Standtall', 'breed': 'quarter horse'},
            {'name': 'Cheyenne', 'breed': 'Stallion'},
            {'name': 'Misty', 'breed': 'standard'},
        ]
        for obj in ponies:
            p = Pony.objects.create(**obj)

        user = User.objects.create(username='test', email='test@gmail.com', is_staff=True)
        user.set_password('test')
        user.save()


    def test_ajax_view(self):
        """
        Test that the view works properly.
        """
        self.client.login(username='test', password='test')
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('chosen_lookup')
        get_data = {'q': 'sta', 'model': 'pony', 'app': 'chosen', 'fields': 'name breed'}
        response = self.client.get(url, get_data, **kwargs)

        json_string = response.content
        data = json.loads(json_string)  
        
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['text'], u'Star')
        self.assertEqual(data[1]['text'], u'Standtall')
        self.assertEqual(data[3]['text'], u'Misty')

