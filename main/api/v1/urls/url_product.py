from django.urls import path, re_path, include
from main.api.v1.views import view_product as views


urlpatterns = [

    path('list',
         views.ProductListAPIView.as_view(),
         name='product_list'),

    path('create',
             views.ProductCreateAPIView.as_view(),
             name='product_create'),
     
    path('<int:pk>/',
         views.ProductRetrieveUpdateAPIView.as_view(),
         name='product_retrieve_update_destroy_by_pk'),

    path('<slug:name>/',
             views.ProductRetrieveUpdateAPIView.as_view(),
             name='product_retrieve_update_destroy_by_name'),

]
