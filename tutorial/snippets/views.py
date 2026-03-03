from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


@api_view(["GET"])
def api_root(request, format=None):
    """
    Single entry point listing all top-level URLs in the API.
    reverse() builds fully-qualified absolute URLs using the named patterns
    declared in snippets/urls.py and the incoming request for the hostname.
    """
    return Response(
        {
            "users":    reverse("user-list",    request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


class SnippetHighlight(generics.GenericAPIView):
    """
    Returns the pre-rendered pygments HTML for a single snippet.
    StaticHTMLRenderer bypasses DRF's normal JSON rendering pipeline and
    returns the raw string stored in snippet.highlighted as text/html.
    """
    queryset         = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class SnippetList(generics.ListCreateAPIView):
    queryset           = Snippet.objects.all()
    serializer_class   = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Snippet.objects.all()
    serializer_class   = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]


class UserList(generics.ListAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer
