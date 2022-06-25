"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import notifications.urls
from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any

from rest_framework.views import Response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]


def api_exception_handler(exc, context):
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "error": {
                "status_code": 0,
                "server_message": "",
                "data_errors": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        # We define the user_error in the views def or class itself.
        error["status_code"] = status_code
        error["server_message"] = http_code_to_message[status_code]
        error["data_errors"] = response.data
        response.data = error_payload

    return response