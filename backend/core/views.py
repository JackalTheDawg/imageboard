from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status

from .serializers import *
from .utility.utility import QueryHandler


class CreateUser(APIView):

    permission_classes = [AllowAny]

    def options(self, requset):
        return HttpResponse(headers={
            "Allow": "POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        })

    def post(self, request):
        try:
            CustomUser.objects.create_user(email=request.data['email'],
                                           password=request.data['password'])

            user = CustomUser.objects.get(email=request.data['email'])

            Profile.objects.create(
                user=user,
                name=request.data['name'],
                surname=request.data['surname'],
                gender=request.data['gender'],
                birthday=request.data['birthday']
            )

        except Exception as ex:
            raise ValueError(ex)

        return Response(status=status.HTTP_201_CREATED, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        })


class ApplicationInterface(APIView, QueryHandler):

    def options(self, requset):
        return HttpResponse(headers={
            "Allow": "GET",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        })

    def get(self, request, query, value=None):

        methods = {
            'profile': self.profile_data,
            'community': self.community_data,
            'profiles': self.profile_list,
            'communities': self.community_list,
            'favorites': self.favorite_posts,
        }

        try:
            result = methods[query](value or request.user.id)

            return Response(result, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            })

        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        self.create_record(request)

        return Response(status=status.HTTP_200_OK, headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            })

    def put(self, request):

        self.edit_settings(request)

        return HttpResponse(headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            })

