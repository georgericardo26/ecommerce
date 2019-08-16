from django.urls import path, re_path, include
from main.api.v1.views import view_user as views


urlpatterns = [

    path('list',
         views.UserList.as_view(),
         name='user_list'),
     
    # path('<int:pk>/',
    #      views.UserView.as_view(),
    #      name='user_retrieve_update_destroy_destroy_by_pk'),

    # path('<slug:username>/',
    #      views.UserView.as_view(),
    #      name='user_retrieve_update_destroy_by_username'),

    # re_path(r'^(?P<email>[\w.@+-]+)/$',
    #         views.UserView.as_view(),
    #         name='user_retrieve_update_destroy_by_email'),

    path('alterpassword/<int:pk>/',
         views.UserAlterPasswordView.as_view(),
         name='user_alter_password')

]
