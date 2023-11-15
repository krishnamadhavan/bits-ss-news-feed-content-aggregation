import logging

from django.http import HttpResponse, HttpResponseServerError

logger = logging.getLogger(__name__)


class HealthCheckMiddleware:
    """
    https://www.ianlewis.org/en/kubernetes-health-checks-django
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            if request.path == "/liveness":
                return self.liveness(request)
            elif request.path == "/readiness":
                return self.readiness(request)
        return self.get_response(request)

    @staticmethod
    def liveness(request):
        """
        Returns that the server is alive.
        """
        return HttpResponse("OK")

    @staticmethod
    def readiness(request):
        """
        Connect to each database and do a generic standard SQL query
        that doesn't write any data and doesn't depend on any tables
        being present.
        """
        try:
            from django.db import connections

            for name in connections:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return HttpResponseServerError("MySQL: Returned invalid response.")
        except Exception as e:
            logger.exception(e)
            return HttpResponseServerError("MySQL: Cannot connect to the database.")

        try:
            from django_redis import get_redis_connection

            get_redis_connection("default")
        except Exception as e:
            logger.exception(e)
            return HttpResponseServerError("Redis: Cannot connect to the database.")

        return HttpResponse("OK")
