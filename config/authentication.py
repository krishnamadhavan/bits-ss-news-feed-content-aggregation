import logging

import jwt
import requests
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from config import constants

from config.tasks import update_userinfo

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        # Decode the access_token and get the user payload using public_key
        access_token = auth[1]
        url = f"{constants.AUTH_SERVICE_URL}/api/auth/jwt/verify/"
        payload = {
            "token": access_token
        }
        resp = requests.post(url=url, data=payload)
        if resp.status_code != 200:
            detail = (
                "The provided authorization grant (e.g., authorization code, resource owner credentials) or "
                "refresh token is invalid, expired, revoked, does not match the redirection URI used in the "
                "authorization request, or was issued to another client. "
            )
            raise exceptions.NotAuthenticated(detail=detail)

        decoded_payload = jwt.decode(access_token, algorithms=["HS256"], options={"verify_signature": False})
        return self.authenticate_credentials(decoded_payload)

    def authenticate_credentials(self, userinfo):
        defaults = {
            "email": userinfo["email"],
            "username": userinfo["username"],
            "first_name": userinfo["first_name"],
            "last_name": userinfo["last_name"],
            "is_superuser": userinfo["is_superuser"],
            "is_active": userinfo["is_active"]
        }
        user, created = User.objects.get_or_create(
            username=userinfo["username"], defaults=defaults
        )

        if not created:
            # On the best effort basis, keep the user information updated with the Source of Truth (SSO).
            update_userinfo.delay(
                email=userinfo["email"],
                username=userinfo["username"],
                first_name=userinfo["first_name"],
                last_name=userinfo["last_name"],
                is_superuser=userinfo["is_superuser"],
                is_active=userinfo["is_active"],
            )
        return user, None
