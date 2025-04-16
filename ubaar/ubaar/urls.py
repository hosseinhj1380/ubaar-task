"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
# from user_module.views import UserLogView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/",include("config.urls_v1"), name="v1"),
    # path("api/v2/",include("config.urls_v2"), name="v2"),

    
]




if settings.DEBUG:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from drf_yasg.generators import OpenAPISchemaGenerator

    class MultipleSchemesSchemaGenerator(OpenAPISchemaGenerator):
        def get_schema(self, request=None, public=False):
            schema = super().get_schema(request, public)
            schema.schemes = ["http", "https"]  # Allow both HTTP and HTTPS
            return schema

    # Use this generator in the schema view
    schema_view = get_schema_view(
        openapi.Info(
            title="Your API",
            default_version="v1",
        ),
        public=True,
        generator_class=MultipleSchemesSchemaGenerator,  # Use custom generator
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += [
        path(
            "docs/",
            csrf_exempt(schema_view.with_ui("swagger", cache_timeout=0)),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
        path(
            "swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
    ]
