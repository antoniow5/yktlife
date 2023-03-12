"""yktlife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from forum import views as forum_views


from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any

from rest_framework.views import Response


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/v1/forum/categories/$', forum_views.categories_list),
    path('api/v1/forum/categories/<str:slug>', forum_views.categories_detail),
    path('api/v1/forum/categories/<str:slug>/', forum_views.categories_detail),
    
    re_path('api/v1/forum/topics/$', forum_views.topics_list),
    path('api/v1/forum/topics/<int:id>', forum_views.topics_detail),
    path('api/v1/forum/topics/<int:id>/', forum_views.topics_detail),

    
    path('__debug__/', include('debug_toolbar.urls'))
]

def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
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
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    return response

