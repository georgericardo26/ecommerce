from django.urls import include, path, re_path

urlpatterns = [
    path('v1/', include('main.api.urls.v1_urls')),
]
