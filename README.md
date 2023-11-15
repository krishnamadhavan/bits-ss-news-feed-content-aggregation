# News Feed Content Aggregation Service

Django backend for managing user search on courses and provide data to analytics engine

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Basic Commands

### Setting Up Your Users

- To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

### Type checks

Running type checks with mypy:

    $ mypy news_feed_content

### Sort imports

Running sort import statement with isort:

    $ isort .

### Code styles

Running code style checks with black:

    $ black .

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd news_feed_content
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

## Development

The following details how to configure your development environment.

### Docker

See detailed [Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html).

## Deployment

To deploy this application to OpenShift, please follow the steps below:

- Login into OpenShift using `oc login` and navigate to the namespace of interest using `oc project <namespace>`
- Now, `cd shell-scripts`, update the `version` and run the shell script using `sh build-django-image.sh`
- Update the version in `image.tag` in `charts/values.yaml`.
- Now, from the root folder install the app using `helm install news-feed-content chart --namespace=<namespace> --dependency-update`.
- We can make changes to the application and install a new version using `helm upgrade news-feed-content chart --namespace=<namespace> --dependency-update`
