from django.urls import path, re_path, include
from main.api.v1.views import view_request as views


urlpatterns = [

    path('list',
         views.RequestListAPIView.as_view(),
         name='request_list'),

    path('create',
             views.RequestCreateAPIView.as_view(),
             name='request_create'),

    path('<int:pk>/',
         views.RequestRetrieveUpdateAPIView.as_view(),
         name='request_retrieve_update_destroy_by_pk'),

]
