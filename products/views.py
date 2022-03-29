from django.shortcuts import render
from products.models import (
    Product,
    Category,
    Size,
    Brand,
    UnitofMeasure,
    ProductImage,
)
from rest_framework import status
from products.filterset import ProductFilter
from products.serializers import (
    ProductSerializer,
    CategorySerializer,
    BrandSerializer,
    UoMSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    )
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from googletrans import Translator

translator = Translator()


# ListAPI View of Product-Category.
class CategoryListApiView(ListAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("name")
    # ordering_fields = ("created_at")
    queryset = Category.objects.all()


# RetrieveAPI View of Product_Category
class CategoryAPIView(RetrieveAPIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {}
        for k, v in serializer.data.items():
            data = translator.translate(str(v), dest='ar').text

        return Response(data)

class CategoryInfo(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny, ]

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        try:
            instance = self.get_object()
            category_info = {
                "id": instance.id,
                "Name": instance.name,
                "image": instance.categoryImage.url
            }
            return Response({"status": True, "data": category_info}, status=status.HTTP_200_OK)
        except (Exception) as e:
            print(e)
            return Response({"status": False, "data": {"msg": "Category not found."}}, status=status.HTTP_404_NOT_FOUND)



# CreateAPI View of Product-Category.
class CategoryCreateAPIView(APIView):
    pass



class ProductView(APIView):

    """ API for Product """

    def get(self, request):
        category = self.request.query_params.get('category')
        if category:
            queryset = Product.objects.filter(category__id = category)
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) , 'data' : serializer.data})

# Product List According to Category
class CategoryProductList(APIView):

    def get(request, cat_id):
        # category = self.request.query_params.get('category')
        category= Category.objects.get(id=cat_id)
        data=Product.objects.filter(category=category).order_by('-id')
        # data = Product.objects.filter(category=category)
        return Response(
             request,
             {
			'data':data,
			}
    )

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',
                  {
			'data':data,
			}
    )

class ProductbyBrandView(APIView):

    """ API for Productbybrand """

    def get(self, request):
        brand = self.request.query_params.get('brand_name')
        if brand:
            queryset = Product.objects.filter(brand_name__id = brand)
        else:
            queryset = Product.objects.all()
        serializer = ProductSerializer(queryset , many = True)
        return Response({'count' : len(serializer.data) , 'data' : serializer.data})


class ProductsByCategory(ListAPIView):

    serializer_class = ProductSerializer
    # permission_classes = (AllowAny,)

    """
    Returns products under a single category in `slug`
    Endpoint: `api/store/category/<slug>`
    """

    def get_queryset(self):
        return Product.objects.filter(
            category__in=Category.objects.get(id=self.kwargs["id"]).get_descendants(include_self=True)
        )


# Create your views here.
class ProductListAPIView(ListAPIView):

    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = ProductFilter

    search_fields = ("name", "sku", "barcode","category","brand")
    ordering_fields = ("-id")