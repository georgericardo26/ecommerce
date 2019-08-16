from django.urls import path, re_path, include
from main.api.v1.views import view_product_type as views


urlpatterns = [

    path('list',
         views.ProductTypeListAPIView.as_view(),
         name='product_type_list'),

    path('create',
             views.ProductTypeCreateAPIView.as_view(),
             name='product_type_create'),
     
    path('<int:pk>/',
         views.ProductTypeRetrieveUpdateAPIView.as_view(),
         name='product_type_retrieve_update_destroy_by_pk'),

    path('<slug:name>/',
             views.ProductTypeRetrieveUpdateAPIView.as_view(),
             name='product_type_retrieve_update_destroy_by_name'),

]
