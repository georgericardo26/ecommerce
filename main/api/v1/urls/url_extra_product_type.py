from django.urls import path, re_path, include
from main.api.v1.views import view_extra_product_type as views


urlpatterns = [

    path('list',
         views.ExtraProductTypeListAPIView.as_view(),
         name='extra_product_list'),

    path('create',
             views.ExtraProductTypeCreateAPIView.as_view(),
             name='extra_product_create'),
     
    path('<int:pk>/',
         views.ExtraProductTypeRetrieveUpdateAPIView.as_view(),
         name='extra_product_retrieve_update_destroy_by_pk'),

    path('<slug:name>/',
             views.ExtraProductTypeRetrieveUpdateAPIView.as_view(),
             name='extra_product_retrieve_update_destroy_by_name'),

]
