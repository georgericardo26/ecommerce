from django.urls import path, re_path, include
from main.api.v1.views import view_brand as views


urlpatterns = [

    path('list',
         views.BrandListAPIView.as_view(),
         name='brand_list'),

    path('create',
             views.BrandCreateAPIView.as_view(),
             name='brand_create'),
     
    path('<int:pk>/',
         views.BrandRetrieveUpdateAPIView.as_view(),
         name='brand_retrieve_update_destroy_by_pk'),


]
