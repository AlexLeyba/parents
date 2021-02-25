from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="Родитель 48", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("workshop/", include("workshop.urls")),
    path("users/", include("users.urls")),
    path("faq/", include("faq.urls")),
    path("alphabet/", include("alphabet.urls")),
    path("consultation/", include("consultation.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Администрирование сайта roditel48.ru"
admin.site.site_title = "Администрирование сайта roditel48.ru"
admin.site.index_title = "Администрирование сайта"
