from django.urls import path, re_path, include
from main.api.v1.views import view_user as views


urlpatterns = [

    path('list',
         views.UserList.as_view(),
         name='user_list'),

    path('alterpassword/<int:pk>/',
         views.UserAlterPasswordView.as_view(),
         name='user_alter_password')

]
