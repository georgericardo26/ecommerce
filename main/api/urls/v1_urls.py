from django.urls import include, path, re_path
from rest_framework import permissions
from main.api.v1.views.view_auth import AuthView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API Test",
        default_version='v1',
        description="API REST para ecommerce, projeto teste",
        terms_of_service="#",
        contact=openapi.Contact(email="georgericardo26@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'v1'
urlpatterns = [
    path('user/', include('main.api.v1.urls.url_user')),
    path('auth', AuthView.as_view(), name="authentication"),
    path('client/', include('main.api.v1.urls.url_client')),
    path('brand/', include('main.api.v1.urls.url_brand')),
    path('extra_type/', include('main.api.v1.urls.url_extra_product_type')),
    path('product_type/', include('main.api.v1.urls.url_product_type')),
    path('product/', include('main.api.v1.urls.url_product')),
    path('request/', include('main.api.v1.urls.url_request')),

    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]