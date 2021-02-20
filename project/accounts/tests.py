import json
from django.test import TestCase
from django.urls import reverse


class AccountsTest(TestCase):

    def test_signup(self):
        # success
        response = self.client.post(path=reverse('signup'), data={'username': 'gapgit', 'password': 123456})
        assert response.status_code == 200
        assert json.loads(response.getvalue()).get('token') is not None

        # duplicated username
        response = self.client.post(path=reverse('signup'), data={'username': 'gapgit', 'password': 1234})
        assert response.status_code == 400
        assert response.getvalue().decode() == 'Duplicate email'

        # invalid body
        response = self.client.post(path=reverse('signup'), data={'password': 123456})
        assert response.status_code == 400

        # not allowed method
        response = self.client.get(path=reverse('signup'))
        assert response.status_code == 405

