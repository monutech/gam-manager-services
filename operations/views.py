from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Group, Object, Order
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ObjectSerializer, GroupSerializer, OrderSerializer


class Group(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class Object(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

    @action(detail=True, methods=["POST"])
    def set_filter(self, pk, request):
        print(pk)
        print(request)
        return Response(200)


class Order(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer