from django.urls import include, path, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

app_name = "project"
urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls, name="admin_page"),
    path('api/', include('main.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
