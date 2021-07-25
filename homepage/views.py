from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from orders.views import UserCheckout

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 2 > customize the TokenObtainPairSerializer to show up more information
    def validate(self, attrs):
        data = super().validate(attrs)

        #refresh = self.get_token(self.user)

        # super will get the refresh and access tokens and all the below are additional to the data response 
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        data['braintree_id'] = UserCheckout.objects.get(user=self.user.id).get_braintree_id

        return data
    
    # 1 > default customization as per the documentation 
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'Token message'
    #     token['email'] = user.email

    #     return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer