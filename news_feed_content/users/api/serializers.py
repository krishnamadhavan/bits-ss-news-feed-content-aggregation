from rest_framework import serializers

from news_feed_content.users import models


class ContentProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentProviders
        fields = "__all__"


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contents
        fields = "__all__"
