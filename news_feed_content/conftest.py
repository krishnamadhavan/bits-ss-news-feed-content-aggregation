import pytest
from django.contrib.auth.models import User

from news_feed_content.users.tests.factories import (
    UserFactory,
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()
