from django.http import HttpRequest


class MockRequest(HttpRequest):

    def __init__(self, *args, **kwargs):
        super(MockRequest, self).__init__()
        self.META = kwargs.get('META')