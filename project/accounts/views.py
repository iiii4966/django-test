from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed
)

from accounts.models import User
from core.authentication import JWTAuthenticator


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if None in [username, password]:
            return HttpResponseBadRequest(content='Invalid data request')

        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest(content='Duplicate email')

        user = User.objects.create_user(
            username=username,
            password=password,
        )

        return JsonResponse(data={'user_id': user.id, 'token': JWTAuthenticator.encode_token(user=user)})
    return HttpResponseNotAllowed(permitted_methods=['POST'])
