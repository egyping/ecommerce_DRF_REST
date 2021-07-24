from django.shortcuts import render

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 2 > customize the TokenObtainPairSerializer to show up more information
    def validate(self, attrs):
        data = super().validate(attrs)

        #refresh = self.get_token(self.user)

        data['username'] = self.user.username
        data['email'] = self.user.email

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