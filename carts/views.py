from django.shortcuts import get_object_or_404, render

from .models import Cart, CartItem
import base64
from rest_framework.response import Response
from rest_framework.views import APIView
from base64 import encode
import ast
from django.http import Http404
from catalog.models import Variation



class CartUpdateAPIMixin(object):
        def update_cart(self, *args, **kwargs):
            request = self.request
            cart = self.cart
            if cart:
                item_id = request.GET.get("item")
                delete_item = request.GET.get("delete", False)
                flash_message = ""
                item_added = False


                # if the item exist in the get call 
                if item_id:
                    # Using the item id get the exact variation
                    item_instance = get_object_or_404(Variation, id=item_id)
                    # get the quantity from the request
                    qty = request.GET.get("qty", 1)
                    # if the quantity 0 or - make the delete_item True
                    try:
                        if int(qty) < 1:
                            delete_item = True
                    except:
                        raise Http404
                    # 
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
                    if created:
                        flash_message = "Successfully added to the cart"
                        item_added = True
                    # if delete_item marked true before 
                    if delete_item:
                        flash_message = "Item removed successfully."
                        cart_item.delete()
                    else:
                        if not created:
                            flash_message = "Quantity has been updated successfully."
                        cart_item.quantity = qty
                        cart_item.save()


class CartAPIView(CartUpdateAPIMixin, APIView):
    token = None
    cart = None

    def create_token(self, cart_id):
        data = {
            "cart_id": cart_id
        }
        token = base64.standard_b64encode(str(data).encode("utf-8")).decode("utf-8")
        self.token = token
        return token

    # 
    def get_cart(self):
        # if the token exist get it from the request
        token_data = self.request.GET.get('token')
        # create dummy cart
        cart_obj = None

        # if the get request has token, decode it, get cart_id, return cart object
        if token_data:
            token_dict = ast.literal_eval(base64.standard_b64decode(token_data.encode("utf-8")).decode("utf-8"))
            cart_id = token_dict.get("cart_id")
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
            self.create_token(cart.id)
            cart_obj = cart
        return cart_obj

    # 
    def get(self, request, format=None):
        # First either i will get the cart data or i wil create new one 
        cart = self.get_cart()
        self.cart = cart
        # if the get call has cart and has item it will update the cart 
        self.update_cart()
        data = {
            "token": self.token,
            "cart" : cart.id,
            "total": cart.total,
            "subtotal": cart.subtotal,
            "tax_total": cart.tax_total,
            "count": cart.items.count(),
            "items": cart.items.count(),

        }
        return Response(data)

# /api/cart/?token=eydjYXJ0X2lkJzogMTh9&item=3&qty=10
