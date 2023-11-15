from django.contrib import admin

from news_feed_content.users import models


@admin.register(models.ContentProviders)
class ContentProvidersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "endpoint_url")
    search_fields = ("name",)


@admin.register(models.Contents)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "title", "short_description", "about", "image_url", "external_content_url", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("provider",)
