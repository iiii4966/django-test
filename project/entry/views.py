import json

from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseForbidden
)
from django.views import View
from entry.models import Post
from core.authentication import jwt_authenticate


class PostCreateListView(View):
    http_method_names = ['get', 'post']

    @jwt_authenticate
    def post(self, request):
        content = request.POST.get('content')

        if content is None:
            return HttpResponseBadRequest(content='Invalid request body')

        post = Post.objects.create(
            user=request.user,
            content=content,
        )

        return JsonResponse(data=post.to_dict)

    def get(self, request):
        return JsonResponse(
            data=[post.to_dict for post in Post.objects.select_related('user')],
            safe=False,
        )


class PostDetailView(View):
    http_method_names = ['get', 'delete', 'patch']

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return HttpResponseNotFound(content='Not exist post')
        if request.method == 'GET':
            return JsonResponse(data=post.to_dict)
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

    @jwt_authenticate
    def delete(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return HttpResponseNotFound(content='Not exist post')
        if request.user.is_owner(post):
            post.delete()
            return HttpResponse(status=200)
        return HttpResponseForbidden()

    @jwt_authenticate
    def patch(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            return HttpResponseNotFound(content='Not exist post')
        if request.user.is_owner(post):
            body = json.loads(request.body)
            content = body.get('content')
            if content is None:
                return HttpResponseBadRequest(content='Invalid request body')
            post.content = content
            post.save(update_fields=['content'])
            return JsonResponse(status=200, data=post.to_dict)
        return HttpResponseForbidden()
