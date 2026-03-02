from django.contrib.auth.models import User
from rest_framework import generics, permissions

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


class SnippetList(generics.ListCreateAPIView):
    queryset           = Snippet.objects.all()
    serializer_class   = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Called by CreateModelMixin.create() after validation.
        # Injects the authenticated user as the snippet owner so the client
        # never has to (and cannot) supply the owner field directly.
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Snippet.objects.all()
    serializer_class   = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]


class UserList(generics.ListAPIView):
    # ListAPIView = read-only list; no POST endpoint
    queryset         = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # RetrieveAPIView = read-only detail; no PUT/DELETE endpoint
    queryset         = User.objects.all()
    serializer_class = UserSerializer
