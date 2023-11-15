import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache

from config.constants import REDIS_CACHE_EXPIRY

User = get_user_model()

logger = logging.getLogger(__name__)


class CacheMixin:
    @staticmethod
    def get_cache(key: str):
        return cache.get(key)

    @staticmethod
    def set_cache(key: str, value: str, timeout: int = REDIS_CACHE_EXPIRY):
        cache.set(key, value, timeout)

    @staticmethod
    def delete_cache(key: str):
        cache.delete(key)
