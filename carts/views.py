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




class CheckoutAPIView(CartTokenMixin, TokenMixin, APIView):
    # GET call, then access the CartTokenMixin
    def get(self, request, format=None):
        data, cart_obj, response_status = self.get_cart_from_token()
        print(cart_obj)
        return Response(data, status=response_status)




class CartAPIView(TokenMixin, CartUpdateAPIMixin, APIView):

    cart = None

    # get the cart from token otherwise create new cart
    def get_cart(self):
        # if the token exist get it from the request
        token_data = self.request.GET.get('token')

        # create dummy cart object
        cart_obj = None

        # if the get request has token, decode it, get cart_id, return cart object
        if token_data:
            # token_dict = ast.literal_eval(base64.standard_b64decode(token_data.encode("utf-8")).decode("utf-8"))
            token_dict = self.parse_token(token=token_data)
            cart_id = token_dict.get("cart_id")
            print(cart_id)
            try:
                cart_obj = Cart.objects.get(id=cart_id)
            except:
                pass
            self.token = token_data


        # If no cart passed in the request it will create new cart object 
        if cart_obj == None:
            cart = Cart()
            cart.tax_percentage = 0.075
            if self.request.user.is_authenticated:
                cart.user = self.request.user
            cart.save()
            data = {
                "cart_id": cart.id,
            }
            # use the create_token from the mixins to create the token for the new cart
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
            
        }
        return Response(data)



