import base64
import ast
from carts.models import CartItem
from django.http import Http404
from rest_framework.generics import get_object_or_404
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
                # we are adding the variation to the cart not the product!
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


class TokenMixin(object):
    token = None
    
    def create_token(self, data_dict):
        if type(data_dict) == type(dict()):
            token = base64.standard_b64encode(str(data_dict).encode("utf-8")).decode("utf-8")
            #token = base64.b64encode(str(data_dict))
            self.token = token
            return token
        else:
            raise ValueError("Creating a token must be a Python dictionary.")


    def parse_token(self, token=None):
        if token is None:
            return {}
        try:
            token_data = self.request.GET.get('token')
            token_dict = ast.literal_eval(base64.standard_b64decode(token_data.encode("utf-8")).decode("utf-8"))

            return token_dict
        except:
            return {}