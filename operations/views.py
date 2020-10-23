from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Group, Object
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.
class Group(viewsets.ModelViewSet):
    queryset = Group.objects.all()


class Object(viewsets.ModelViewSet):
    queryset = Object.objects.all()

    @action(detail=True, methods=["POST"])
    def set_filter(self, pk, request):
        print(pk)
        print(request)
        return Response(200)

