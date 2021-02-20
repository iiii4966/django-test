from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.PostCreateListView.as_view(), name='post-list-create'),
    path('/<int:post_id>', views.PostDetailView.as_view(), name='post-detail'),
]
