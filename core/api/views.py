from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView
)
from core.models import Comment, Profile, Post
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly
from django.utils import timezone

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # print('curr_post:!!!', serializer.data['id'])
        # print('SERIALIZER DATA!!!!', serializer)
        if self.request.method == "POST":
            curr_post = self.request.data['id']
            p = Post.objects.get(pk=curr_post)
            print("CHHHHHHHHHHHHHHHHECK!", p)
        # p = Post.objects.get(pk=self.request.POST.get('id'))
        serializer.save(user=self.request.user, created=timezone.now(), post=p)


class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentUpdateView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    #     # print('curr_post:!!!', serializer.data['id'])
    #     # print('SERIALIZER DATA!!!!', serializer)
    #     if self.request.method == "PUT":
    #         curr_post = self.request.data['id']
    #         p = Post.objects.get(pk=curr_post)
    #         print("CHHHHHHHHHHHHHHHHECK!", p)
    #     # p = Post.objects.get(pk=self.request.POST.get('id'))
    #     serializer.save(user=self.request.user, created=timezone.now(), post=p)


class CommentDeleteView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
