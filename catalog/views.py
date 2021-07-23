from django.shortcuts import render
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
)

# generics 
from rest_framework import generics
from .pagination import CatalogPagination
from rest_framework import  filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters import FilterSet, CharFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend


# Advanced 
class ProductFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', distinct=True)
    category = CharFilter(field_name='categories__title', lookup_expr='icontains', distinct=True)
    category_id = CharFilter(field_name='categories__id', lookup_expr='icontains', distinct=True)
    min_price = NumberFilter(field_name='price', lookup_expr='gte', distinct=True) 
    max_price = NumberFilter(field_name='price', lookup_expr='lte', distinct=True)
    var_value = CharFilter(field_name='variation__value', lookup_expr='icontains', distinct=True)
    class Meta:
        model = Product
        fields = [
            'min_price',
            'max_price',
            'category',
            'title',
            'description',
        ]

# http://127.0.0.1:8000/api/products/?min_price=90.00&max_price=&category=&title=&description=&category_id=


# Categories views 
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CatalogPagination

    filter_backends = [
                    filters.SearchFilter, 
                    filters.OrderingFilter, 
                    DjangoFilterBackend,
                    ]

    search_fields = ['title']
    ordering_fields = ['title', 'id']
    filter_class = ProductFilter


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

