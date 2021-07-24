
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import (
    CategoryListAPIView,
    CategoryRetrieveAPIView,
    ProductListAPIView,
    ProductRetrieveAPIView
)
from orders.views import UserCheckoutAPI
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from  homepage.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Token 
    path('api/user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls')),

    # Categories APIs
    path('api/categories/', CategoryListAPIView.as_view(), name="categories_list"),
    path('api/categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name="category_details"),

    # Products APIs
    path('api/products/', ProductListAPIView.as_view(), name="products_list"),
    path('api/products/<int:pk>/', ProductRetrieveAPIView.as_view(), name="product_details"),

    # API User 
    path('api/user/checkout/', UserCheckoutAPI.as_view(), name="user_checkout_api"),


    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)