import json
import logging
import time

import requests
from django.contrib.auth import get_user_model

from config import celery_app
from news_feed_content.users import models

logger = logging.getLogger(__name__)

User = get_user_model()


@celery_app.task()
def update_userinfo(
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    is_superuser: bool,
    is_active: bool
):
    user = User.objects.get(username=username)

    context = {
        "email": email,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "is_superuser": is_superuser,
        "is_active": is_active
    }

    for field in [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "is_active"
    ]:
        if getattr(user, field) != context[field]:
            setattr(user, field, context[field])

    user.save()


@celery_app.task()
def fetch_content_metadata() -> bool:
    """
    Fetch content metadata from partner APIs and trigger concurrent requests.

    This function retrieves content providers API information from the database and initiates separate tasks for each
    provider API, making concurrent requests to reduce runtime and utilize multiple Celery workers.

    Returns:
        bool: True if the task was successfully initiated.
    """
    queryset = models.ContentProviders.objects.all()

    for instance in queryset:
        endpoint_url = instance.endpoint_url

        # Triggering separate tasks for each partner API, making concurrent requests
        # which reduces runtime and makes use of multiple workers at the same.
        # As the no. of APIs (partners) increases, we can increase the no. of celery
        # workers.
        call_api_and_insert_data_into_db.delay(
            provider_id=instance.pk, method="GET", url=endpoint_url, headers={}
        )

    return True


@celery_app.task()
def call_api_and_insert_data_into_db(
    provider_id: int, method: str, url: str, headers: str, params: dict or None = None
) -> bool:
    """
    Call a provider API, retrieve data, and insert it into the database.

    This function is responsible for making an API call to a provider's endpoint, retrieving data, and
    inserting course metadata into the database. It also handles pagination and processes data in batches.

    Args:
        provider_id (int): The unique identifier for the provider in the database.
        method (str): The HTTP request method for the API call (e.g., 'GET', 'POST').
        url (str): The URL of the partner's API endpoint.
        headers (str): JSON-formatted headers to include in the API request.
        params (dict or None, optional): Additional query parameters to include in the API request. Default is None.

    Returns:
        bool: True if the API call was successful and data was inserted into the database; otherwise, False.
    """
    # Check if the provider_id is valid early in the method
    # to avoid making unnecessary API calls.
    items = []
    try:
        provider = models.ContentProviders.objects.get(pk=provider_id)
    except models.ContentProviders.DoesNotExist:
        logger.error(f"Partner with partner_id: {provider_id} does not exist.")
        return False

    if params is None:
        params = {"page": 1, "page_size": 50}

    if isinstance(headers, str):
        headers = json.loads(headers)

    # Let's not bombard the endpoint with multiple requests
    time.sleep(2)

    resp = requests.request(method=method, url=url, headers=headers, params=params)
    logger.info(f"Current URL in action: {resp.url}")

    if resp.status_code != 200:
        logger.error(f"Expected status_code is 200, but got {resp.status_code}")
        return False

    # We're mocking it here, since we don't have a realistic endpoint_url to give this data
    # data = resp.json()
    data = {
        "pagination": {
            "next": None,
            "previous": None,
            "count": 5
        },
        "results": [
            {
                "title": "The rise of COVID-19",
                "short_description": "The rise of COVID-19 is at an alarming rate.",
                "about": "The rise of COVID-19 is at an alarming rate.",
                "image_url": "https://fastly.picsum.photos/id/651/200/300.jpg?hmac=0w4DoCrs0gvMucmilCFXoqZAB9P3n94dVJ70mY8A4yQ",
                "external_content_url": "https://example.com"
            }
        ]
    }
    results = data["results"]

    for result in results:
        items.append(
            models.Contents(
                provider=provider,
                title=result["title"],
                short_description=result.get("short_description", None),
                about=result.get("about", None),
                image_url=result["image_url"],
                external_content_url=result.get("external_content_url", None),
            )
        )
    models.Contents.objects.bulk_update_or_create(
        items,
        [
            "provider",
            "title",
            "short_description",
            "about",
            "image_url",
            "external_content_url",
        ],
        match_field="title",
    )

    if data["pagination"]["next"] is not None:
        call_api_and_insert_data_into_db(
            provider_id=provider_id,
            method=method,
            url=url,
            headers=headers,
            params={"page": params["page"] + 1, "page_size": 50},
        )

    return True
