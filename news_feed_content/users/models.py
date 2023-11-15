from django.db import models
from django.utils.translation import gettext_lazy as _

from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(
        _("Created At"), auto_now_add=True, help_text=_("Created Date and Time")
    )
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, help_text=_("Updated Date and Time")
    )

    class Meta:
        abstract = True


class ContentProviders(TimeStampModel):
    name = models.CharField(_("Name of the content provider"), max_length=254)
    endpoint_url = models.URLField(_("API endpoint URL"), max_length=254)

    class Meta:
        db_table = _("content_providers")
        verbose_name = _("Content Provider")
        verbose_name_plural = _("Content Providers")

    def __str__(self):
        return self.name


class Contents(TimeStampModel):
    provider = models.ForeignKey(to=ContentProviders, verbose_name=_("Content Provider"), on_delete=models.CASCADE)
    title = models.CharField(_("Title of the Content"), max_length=254)
    short_description = models.CharField(_("Short description"), max_length=254)
    about = models.TextField(_("Full description an the content"))
    image_url = models.FileField(_("Content Image URL"), upload_to="content-images")
    external_content_url = models.URLField(_("External Content URL"), max_length=254)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        db_table = _("contents")
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __str__(self):
        return self.title
