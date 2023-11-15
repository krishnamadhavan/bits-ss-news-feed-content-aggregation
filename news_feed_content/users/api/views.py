from rest_framework import viewsets, permissions

from news_feed_content.users import models
from news_feed_content.users.api import serializers


class ContentProvidersViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ContentProvidersSerializer
    queryset = models.ContentProviders.objects.all()


class ContentsViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ContentsSerializer
    queryset = models.Contents.objects.all()
