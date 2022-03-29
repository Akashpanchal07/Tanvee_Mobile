from django.contrib import admin
from products.models import Product, Category, Brand, Size, UnitofMeasure, ProductImage

# Register ProductImage models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4
    readonly_fields = ['image_tag']

# Register Category Model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    list_filter = ['name',]
    list_per_page =10
    search_fields = ['name',]
    readonly_fields = ['image_tag',]

admin.site.register(Category, CategoryAdmin)


# Register Product Model
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'brand_name', 'uom', 'short_description',
    ]
    inlines = [ProductImageInline, ]
    list_filter = ['name', 'category', 'brand_name', ]
    list_per_page = 10
    search_fields = ['name', 'category']
admin.site.register(Product, ProductAdmin)
# Register Brand, Size, UnitofMeasure Models, ProductImages
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(UnitofMeasure)
admin.site.register(ProductImage)

