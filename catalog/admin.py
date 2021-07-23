from django.contrib import admin
from .models import Product, Variation, ProductImage, Category

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	max_num = 10

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0
	max_num = 10


class ProductAdmin(admin.ModelAdmin):
	list_display = ['title', 'price', 'slug']
	inlines = [
		ProductImageInline,
		VariationInline,
	]
	class Meta:
		model = Product
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    class Meta:
        model = Category

admin.site.register(Product, ProductAdmin)



admin.site.register(Variation)

admin.site.register(ProductImage)

admin.site.register(Category, CategoryAdmin)



