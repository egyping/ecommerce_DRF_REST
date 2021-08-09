
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import (
    CategoryListAPIView,
    CategoryRetrieveAPIView,
    ProductListAPIView,
    ProductRetrieveAPIView,
)
from carts.views import CartAPIView, CheckoutAPIView
from orders.views import UserCheckoutAPI, UserAddressCreateAPIView, UserAddressListAPIView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from  homepage.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django debug tool bar
    path('__debug__/', include(debug_toolbar.urls)),
    
    # JWT Token => Login API 
    path('api/user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls')),

    # Categories APIs
    path('api/categories/', CategoryListAPIView.as_view(), name="categories_list"),
    path('api/categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name="category_details"),

    # Products APIs
    path('api/products/', ProductListAPIView.as_view(), name="products_list"),
    path('api/products/<int:pk>/', ProductRetrieveAPIView.as_view(), name="product_details"),

    # API for guest checkout who has email only
    path('api/user/checkout/', UserCheckoutAPI.as_view(), name="user_checkout_api"),

    # Cart 
    path('api/cart/', CartAPIView.as_view(), name="cart_api"),

    # Checkout 
    path('api/checkout/', CheckoutAPIView.as_view(), name="checkout_api"),

    # Address create
    path('api/user/address/create/', UserAddressCreateAPIView.as_view(), name="user_address_create"),

    # Address list
    path('api/user/address/list/', UserAddressListAPIView.as_view(), name="user_address_list"),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# user checkout adding user or guest user  
# POST:         http://127.0.0.1:8000/api/user/checkout/
# POST Data:    {"email": "user1@users.com"}

# User address create
# POST: http://127.0.0.1:8000/api/user/address/create/
'''
{
    "user": null,
    "type": null,
    "street": "",
    "city": "",
    "zipcode": ""
}
'''

# user 2
# user1@users.com
# "user_checkout_token": "eydzdWNjZXNzJzogVHJ1ZSwgJ2JyYWludHJlZV9pZCc6ICc1NDQwMTEzMDcnLCAndXNlcl9jaGVja291dF9pZCc6IDJ9",



# User address list for specific user using the user token "user_checkout_token"
# POST: http://127.0.0.1:8000/api/user/address/list/?token=eydzdWNjZXNzJzogVHJ1ZSwgJ2JyYWludHJlZV9pZCc6ICc1NDQwMTEzMDcnLCAndXNlcl9jaGVja291dF9pZCc6IDJ9

# create new cart 
# /api/cart/

# get cart information 
# /api/cart/?token=eydjYXJ0X2lkJzogMTh9

# add item along with quantity 
# /api/cart/?token=eydjYXJ0X2lkJzogMTh9&item=3&qty=10

# delete item from cart 
# /api/cart/?token=eydjYXJ0X2lkJzogMTh9&item=3&qty=10&delete=true

# Checkout API 
# http://127.0.0.1:8000/api/checkout/?token=eydjYXJ0X2lkJzogNDl9&checkout_id=3

