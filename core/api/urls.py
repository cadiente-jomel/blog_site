from django.urls import path, include
from .views import (
    CommentCreateView,
    CommentDetailView,
    CommentListView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/detail/',
         CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/update/',
         CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment-delete'),
]
