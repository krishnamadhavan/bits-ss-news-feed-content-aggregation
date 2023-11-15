from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent  # noqa
# news_feed_content/
APPS_DIR = ROOT_DIR / "news_feed_content"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))


REDIS_CACHE_EXPIRY = env.int("REDIS_CACHE_EXPIRY")
AUTH_SERVICE_URL = env("AUTH_SERVICE_URL")
