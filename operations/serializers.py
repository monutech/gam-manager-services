from rest_framework import serializers
from .models import Object, Group, Order

class ObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Object

        fields = ["name", "gam_name"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group

        fields = ["orders", "line_items", "base_pql"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order

        fields = ["gam_account_no", "order_id", "order_name", "advertiser", "trafficker" ]