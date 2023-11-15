from setuptools import find_packages, setup

setup(
    name="news-feed-content",
    version="0.2.10",
    packages=find_packages(),
    install_requires=[
        # Python
        "pytz==2022.2.1",
        "argon2-cffi==21.3.0",
        "mysqlclient==2.1.1",
        "whitenoise==6.2.0",
        "uvicorn[standard]==0.18.3",
        "PyJWT==2.6.0",
        "cryptography==38.0.4",
        # Django
        "django==3.2.15",
        "django-environ==0.9.0",
        # Django REST Framework
        "djangorestframework==3.14.0",
        "django-cors-headers==3.13.0",
        # DRF-spectacular for api documentation
        "drf-spectacular==0.24.2",
        # Message Broker
        "celery==5.2.7",
        "django-redis==5.2.0",
        "flower==1.2.0",
        "redis==4.3.4",
        # Production.txt
        "gunicorn==20.1.0",
    ],
    scripts=["manage.py"],
)
