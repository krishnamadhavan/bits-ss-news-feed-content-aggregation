import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

User = get_user_model()

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Use this management command to create a superuser from env variables.

    If the superuser account already exists, print a relevant statement
    on the console, instead of raising an error (prevents the flow of `start` script on runtime)
    """

    def handle(self, *args, **options):
        username = settings.SUPERUSER_USERNAME
        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD

        if User.objects.filter(username=username).exists():
            logger.warning("An superuser account with this username already exists.")
            return

        try:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
        except IntegrityError as e:
            logger.warning("Something went wrong while creating the superuser account.")
            logger.error(f"Error: {e}")
            return

        logger.info("Superuser created successfully.")
