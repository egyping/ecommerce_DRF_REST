from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import UserCheckout
from orders.models import UserAddress
from orders.serializers import UserAddressSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from carts.mixins import TokenMixin

User = get_user_model()

# Create view for address model 
class UserAddressCreateAPIView(CreateAPIView):
    model = UserAddress
    serializer_class = UserAddressSerializer


class UserAddressListAPIView(TokenMixin, ListAPIView):
    model = UserAddress
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    # modifying the query to get the exact user addresses
    def get_queryset(self, *args, **kwargs):
        # from the url get token get the token value
        user_checkout_token = self.request.GET.get("token")
        # using TokenMixin.parse_token retrive the user checkout data 
        # {'success': True, 'braintree_id': '544011307', 'user_checkout_id': 2}
        user_checkout_data = self.parse_token(user_checkout_token)
        # get the value of the user_checkout_id in this case object 2
        user_checkout_id = user_checkout_data.get("user_checkout_id")

        # if the user authenticated and has token its straight forward 
        if self.request.user.is_authenticated:
            return UserAddress.objects.filter(user__user=self.request.user)
        # if guest checkout get his aaddresses using the user_checkout_id object
        elif user_checkout_id:
            return UserAddress.objects.filter(user__id=int(user_checkout_id))
        else:
            return []

            
class UserCheckoutMixin(TokenMixin, object):
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
            data["success"]= True
            # it retreive braintree customer ID or generate
            data["braintree_id"] = user_checkout.get_braintree_id

            # The user checkout object ID
            data["user_checkout_id"] = user_checkout.id

            # using TokenMixin.CreateToken create encoded token from the data dictionary
            # This token will be used in the address list api to identify the exact user
            data['user_checkout_token'] = self.create_token(data)
            
            # get_client_token create token using braintree engine
            data["bt_token"] = user_checkout.get_client_token()

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


