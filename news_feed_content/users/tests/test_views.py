from unittest.mock import patch

import pytest
from django.contrib.auth.models import User

from config.authentication import JWTAuthentication
from news_feed_content.users.tests.factories import UserFactory


class TestContentDelivery:
    content_type = "application/json"

    @staticmethod
    def user() -> User:
        return UserFactory(username="johndoe")

    @pytest.mark.django_db
    @patch.object(JWTAuthentication, "authenticate")
    def test_successful_content_delivery(self, mock_authenticate, client):
        user = self.user()
        # Mock the authenticate method to return a valid user
        mock_authenticate.return_value = (user, None)

        path = "/api/contents/"
        resp = client.get(path=path, content_type=self.content_type)
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_content_delivery_with_no_authentication(self, client):
        path = "/api/contents/"
        resp = client.get(path=path, content_type=self.content_type)
        assert resp.status_code == 401
