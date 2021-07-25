from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import UserCheckout


User = get_user_model()


class UserCheckoutMixin(object):
    def user_failure(self, message=None):
        data = {
            "message": "There was an error. Please try again.",
            "success": False
        }
        if message:
            data["message"] = message
        return data


    def get_checkout_data(self, user=None, email=None):
        # If post has only email and the email already engaged with one of the User model instance
        if email and not user:
            user_exists = User.objects.filter(email=email).count()
            if user_exists != 0:
                return self.user_failure(message="This user already exists, please login.")

        data = {}
        user_checkout = None

        # Request has user and not email it will response by the user and user email
        if user and not email:
            if user.is_authenticated:
                user_checkout = UserCheckout.objects.get_or_create(user=user, email=user.email)[0]

        # Guest checkout only email in the POST, it will create UserCheckout or it will retrieve the existing one
        elif email:
            try:
                user_checkout = UserCheckout.objects.get_or_create(email=email)[0]
                if user:
                    user_checkout.user = user
                    user_checkout.save()
            except:
                pass #(instance, created)
        else:
            pass

        if user_checkout:
            data["bt_token"] = user_checkout.get_client_token()
            data["success"]= True
            data["braintree_id"] = user_checkout.get_braintree_id
            data["user_checkout_id"] = user_checkout.id
            
            
            # del data["braintree_id"]
            # del data["user_checkout_id"]
            # data["braintree_client_token"] = user_checkout.get_client_token()

        return data


class UserCheckoutAPI(UserCheckoutMixin, APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        data = self.get_checkout_data(user=request.user)
        return Response(data)

    def post(self, request, format=None):
        data = {}
        email = request.data.get("email")

        # If logged in and app knows the user and email
        if request.user.is_authenticated:
            if email == request.user.email:
                data = self.get_checkout_data(user=request.user, email=email)
            else:
                data = self.get_checkout_data(user=request.user)
        
        # Guest checkout 
        elif email and not request.user.is_authenticated:
            data = self.get_checkout_data(email=email)
        
        # 
        else:
            data = self.user_failure(message="Make sure you are authenticated or using a valid email.")
        return Response(data)


