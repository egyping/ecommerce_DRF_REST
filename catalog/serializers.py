from rest_framework import serializers

from .models import Product, Category, Variation


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            'id',
            'variant',
            'value',
            'sku',
            'inventory'
            ]


class ProductDetailSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    variation_set = VariationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url



class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    url = serializers.HyperlinkedIdentityField(view_name='product_details')
    variation_set = VariationSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set'
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url




# serialize the categories 
# Django is MVC > URL > view >DRF REST< model

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category_details')

    product_set = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'title',
            'description',
            # model_set
            'product_set'
        ] 