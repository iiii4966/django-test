from django.contrib.auth import get_user_model
from django.test import TestCase

from core.authentication import JWTAuthenticator
from utils.mocks import MockRequest


class TestJWTAuthenticator(TestCase):

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create(username='gapgit', password=1234)
        self.request = MockRequest(META={JWTAuthenticator.AUTH_HEADER_NAME: self.test_encode_token()})

    def tearDown(self):
        pass

    def test_encode_token(self):
        token = JWTAuthenticator.encode_token(user=self.user)
        assert token is not None
        return token

    def test_get_raw_token(self):
        raw = JWTAuthenticator.get_raw_token(JWTAuthenticator.get_header(self.request))
        assert raw is not None
        return raw

    def test_authenticate(self):
        assert JWTAuthenticator.authenticate(self.request)
        assert getattr(self.request, 'user') == self.user

    def test_decode_token(self):
        claim = JWTAuthenticator.decode_token(self.test_get_raw_token())
        assert claim.get('user_id') == self.user.id
