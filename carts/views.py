from django.shortcuts import render

from .models import Cart, CartItem
import base64
from rest_framework.response import Response
from rest_framework.views import APIView
from base64 import encode
import ast






class CartAPIView(APIView):
    token = None
    cart = None

    def create_token(self, cart_id):
        data = {
            "cart_id": cart_id
        }
        token = base64.standard_b64encode(str(data).encode("utf-8")).decode("utf-8")
        self.token = token
        return token

    def get_cart(self):
        
        token_data = self.request.GET.get('token')
        cart_obj = None

        if token_data:
            token_dict = ast.literal_eval(base64.standard_b64decode(token_data.encode("utf-8")).decode("utf-8"))
            cart_id = token_dict.get("cart_id")
            try:
                cart_obj = Cart.objects.get(id=cart_id)
            except:
                pass
            self.token = token_data

        if cart_obj == None:
            cart = Cart()
            cart.tax_percentage = 0.075
            if self.request.user.is_authenticated:
                cart.user = self.request.user
            cart.save()
            self.create_token(cart.id)
            cart_obj = cart

        return cart_obj

    def get(self, request, format=None):
        cart = self.get_cart()
        self.cart = cart
        data = {
            "token": self.token,
            "cart" : cart.id,
            "total": cart.total,
            "subtotal": cart.subtotal,
            "tax_total": cart.tax_total,
            "count": cart.items.count(),
            "items": cart.items.count()
        }
        return Response(data)
