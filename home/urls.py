from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post_detail/<int:post_id>/,<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('delete_post/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('update_post/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/post/', views.PostCreateView.as_view(), name='post_create'),
    path('reply/comment/<int:post_id>/<int:comment_id>/', views.ReplayCommentView.as_view(), name='post_reply'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like'),
]