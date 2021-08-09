

from rest_framework import serializers

from carts.mixins import TokenMixin

from .models import UserAddress, Order



class OrderSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shipping_address",
            "billing_address",
            "shipping_total_price",
            "subtotal",
            "order_total",
        ]
    # obj here is the order
    def get_subtotal(self, obj):
        return obj.cart.subtotal


class UserAddressSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserAddress
            fields = [
                "id",
                "user",
                "type",
                "street",
                "city",
                "zipcode",
            ]