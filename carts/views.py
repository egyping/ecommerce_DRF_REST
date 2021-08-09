from django.shortcuts import get_object_or_404, render

from .models import Cart, CartItem
import base64
from rest_framework.response import Response
from rest_framework.views import APIView
from base64 import encode
import ast
from django.http import Http404
from catalog.models import Variation

from.serializers import CartItemSerializer
from .mixins import TokenMixin, CartUpdateAPIMixin, CartTokenMixin
from rest_framework import status
from orders.models import UserCheckout, Order, UserAddress

from orders.serializers import OrderSerializer, UserAddressSerializer




class CheckoutAPIView(CartTokenMixin, APIView):
    # GET call, then access the CartTokenMixin
    def get(self, request, format=None):
        # using the token get the cart data by using CartTokenMixin.get_cart_from_token
        data, cart_obj, response_status = self.get_cart_from_token()

        # getting the user checkout id from the GET call 
        user_checkout_id = request.GET.get("checkout_id")
        try:
            user_checkout = UserCheckout.objects.get(id = int(user_checkout_id))
        except:
            user_checkout = None
        
        # if no user in the GET call return error on the spot
        if user_checkout == None:
                data = {
                    "message": "A valid user or guest user is required"
                }
                response_status = status.HTTP_400_BAD_REQUEST
                # return and don't continue
                return Response(data, status=response_status)


        if cart_obj:
            if cart_obj.items.count() == 0:
                data = {
                    "message": "Your cart is empty"
                }
                response_status = status.HTTP_400_BAD_REQUEST

            else:
                # get the order or create it
                order, created = Order.objects.get_or_create(cart=cart_obj)
                # if the order is paid return message
                if order.is_complete:
                    # to mark the cart.active false
                    order.cart.is_complete()
                    data = {
                        "message": "This order has been complete"
                    }

                    return Response(data)
                
                #Order created save it
                order.save()

                # use serializer to return data
                data = OrderSerializer(order).data

                # the below data['field_name'] to response the JSON BUT its better to use the above serializer
                # data["order"] = order.id
                # data["user"] = order.user
                # data["shipping_address"] = order.shipping_address
                # data["billing_address"] = order.billing_address
                # data["shipping_total_price"] = order.shipping_total_price
                # data["subtotal"] = cart_obj.total
                # data["total"] = order.order_total


        return Response(data, status=response_status)



class CartAPIView(CartTokenMixin, CartUpdateAPIMixin, APIView):
    cart = None
    # get the cart from token otherwise create new cart
    def get_cart(self):
        # use the CartTokenMixin to get the cart data or return error 
        data, cart_obj, response_status = self.get_cart_from_token()

        # If no cart passed from CartTokenMixin then we will create one
        # and if the retreived cart is not active it will create new cart
        if cart_obj == None or not cart_obj.active:
            # new cart instance
            cart = Cart()
            cart.tax_percentage = 0.075
            if self.request.user.is_authenticated:
                cart.user = self.request.user
            cart.save()
            data = {
                "cart_id": cart.id,
            }
            # use the create_token from CartUpdateAPIMixin to create the token for the new cart
            self.create_token(data)
            cart_obj = cart
        return cart_obj

    # The entry point for /cart/ API to create & update cart
    def get(self, request, format=None):
        # First either i will get the cart data or i wil create new one 
        cart = self.get_cart()
        self.cart = cart
        # if the get call has cart and has item it will update the cart 
        self.update_cart()

        # getting the cart items through serializer 
        items = CartItemSerializer(cart.cartitem_set.all(), many=True)
        data = {
            "token": self.token,
            "cart" : cart.id,
            "count": cart.items.count(),
            "items": items.data,
            "total": cart.total,
            "subtotal": cart.subtotal,
            "tax_total": cart.tax_total,
            "active": cart.active,
            
        }
        return Response(data)

