import json

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from core.authentication import JWTAuthenticator
from entry.models import Post


class EntryTest(TestCase):
    create_list_view_url = 'post-list-create'
    detail_view_url = 'post-detail'

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create(username='gapgit', password=1234)
        self.token = JWTAuthenticator.encode_token(user=self.user)

    @staticmethod
    def field_check(data):
        assert data.get('id') is not None
        assert data.get('user') is not None
        assert data['user'].get('id') is not None
        assert data['user'].get('username') is not None
        assert data.get('content') is not None
        assert data.get('created_at') is not None

    def test_write_post(self):
        body = {'content': 'Hello World!'}

        # success
        response = self.client.post(reverse(self.create_list_view_url), body, Authorization=self.token)
        assert response.status_code == 200
        data = json.loads(response.getvalue())
        self.field_check(data)
        assert data['content'] == body['content']

        # not auth
        response = self.client.post(reverse(self.create_list_view_url), body)
        assert response.status_code == 401

        # not allowed method
        response = self.client.delete(reverse(self.create_list_view_url), Authorization=self.token)
        assert response.status_code == 405

    def test_get_posts(self):
        for i in range(3):
            Post.objects.create(user=self.user, content='Hello World')

        response = self.client.get(reverse(self.create_list_view_url))
        assert response.status_code == 200

        data = json.loads(response.getvalue())

        assert len(data) == 3
        self.field_check(data[0])

    def test_get_post(self):
        post = Post.objects.create(user=self.user, content='Hello World')

        response = self.client.get(reverse(self.detail_view_url, args=[post.id]))
        assert response.status_code == 200
        data = json.loads(response.getvalue())
        self.field_check(data)

    def test_delete_post(self):
        # success
        post = Post.objects.create(user=self.user, content='Hello World')

        response = self.client.delete(reverse(self.detail_view_url, args=[post.id]), Authorization=self.token)
        assert response.status_code == 200
        assert not Post.objects.exists()

        # not auth
        post = Post.objects.create(user=self.user, content='Hello World')

        response = self.client.delete(reverse(self.detail_view_url, args=[post.id]))
        assert response.status_code == 401
        assert Post.objects.exists()

        # when req.user are not a writer
        post = Post.objects.create(user=self.user, content='Hello World')
        other = self.user_model.objects.create(username='gapgit2', password=1234)
        token = JWTAuthenticator.encode_token(user=other)

        response = self.client.delete(reverse(self.detail_view_url, args=[post.id]), Authorization=token)
        assert response.status_code == 403
        assert Post.objects.exists()

    def test_update_post(self):
        # success
        post = Post.objects.create(user=self.user, content='Hello World')

        body = {'content': 'hi'}

        response = self.client.patch(
            reverse(self.detail_view_url, args=[post.id]),
            data=json.dumps(body),
            content_type='application/json',
            Authorization=self.token
        )

        assert response.status_code == 200
        self.field_check(json.loads(response.getvalue()))
        assert Post.objects.first().content == body['content']

        response = self.client.patch(
            reverse(self.detail_view_url, args=[post.id]),
            data=json.dumps(body),
            content_type='application/json',
        )

        assert response.status_code == 401
        assert Post.objects.first().content == body['content']

        # when req.user not a writer
        post = Post.objects.create(user=self.user, content='Hello World')
        other = self.user_model.objects.create(username='gapgit2', password=1234)
        token = JWTAuthenticator.encode_token(user=other)

        response = self.client.patch(
            reverse(self.detail_view_url, args=[post.id]),
            data=json.dumps(body),
            content_type='application/json',
            Authorization=token
        )
        post.refresh_from_db()

        assert response.status_code == 403
        assert post.content == 'Hello World'
