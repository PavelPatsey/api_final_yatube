from posts.models import Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
