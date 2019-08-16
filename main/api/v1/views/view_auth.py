import requests
from django.http import HttpRequest
from django.urls import reverse
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Q

# from main.api.v1.serializers.serializers import CLient
from rest_framework.utils import json

from main.api.v1.serializers.serializer_auth import AuthSerializer
from main.api.v1.serializers.serializer_user import UserSerializer
from main.models import User

PROFILES = ["client"]


class AuthView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        try:
            user = authenticate(username=request.data["username"],
                                    password=request.data["password"])

            obj = {
                    "client_id": request.data["client_id"],
                    "client_secret": request.data["client_secret"],
                    "grant_type": "password",
                    "username": request.data["username"],
                    "password": request.data["password"]
            }

            if user:
                request_api = requests.post(request.build_absolute_uri(reverse('oauth2_provider:token')),
                                        data=json.dumps(obj))

                return Response(request_api.json())

            return Response({"error_details": "user or password be wrong"}, status.HTTP_401_UNAUTHORIZED)

        except Exception as e:

            return Response("Server error! {}".format(e),

                            status.HTTP_500_INTERNAL_SERVER_ERROR)


