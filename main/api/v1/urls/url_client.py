from django.urls import path, re_path, include
from main.api.v1.views import view_client as views


urlpatterns = [

    path('list',
         views.ClientListAPIView.as_view(),
         name='client_list'),

    path('create',
             views.ClientCreateAPIView.as_view(),
             name='client_create'),
     
    path('<int:pk>/',
         views.ClientRetrieveUpdateDestroyAPIView.as_view(),
         name='client_retrieve_update_destroy_by_pk'),

    path('<slug:user__username>/',
             views.ClientRetrieveUpdateDestroyAPIView.as_view(),
             name='client_retrieve_update_destroy_by_username'),

]
