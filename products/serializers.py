from rest_framework import serializers
from products.models import Product, Category, ProductImage, Size, Brand, UnitofMeasure

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = '__all__'            # all Category models field(data)
        exclude = ('created_at', 'updated_at')  # exclude these fields and show all data.


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        # fields = '__all__'                        # all Brand models field(data)
        exclude = ('created_at', 'updated_at')       # exclude these fields and show all data.


# UnitOfMeasure Serializer
class UoMSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitofMeasure
        # fields = '__all__'                      # all Uom models field(data)
        exclude = ('created_at', 'updated_at')  # exclude these fields and show all data.

# Size Serializer
class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        # fields = '__all__'                     # all Uom models field(data)
        exclude = ('created_at', 'updated_at')    # exclude these fields and show all data.


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()       # serialize the category fields of Product Model
    brand_name = BrandSerializer()              # serialize the brand fields of Product Model
    uom = UoMSerializer()                   # serialize the uom fields of Product Model
    sizes = SizeSerializer()                  # serialize the size_type fields of Product Model

    class Meta :
        model = Product
        # fields = '__all__'                                         # all Product models field(data)
        exclude = ('created_at', 'updated_at', 'soft_delete')         # exclude these fields and show all data.