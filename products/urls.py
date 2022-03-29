from django.urls import path
from products import views


app_name = 'products'

urlpatterns = [
    # Category Urls
    path("category-list/", views.CategoryListApiView.as_view()),
    # path("category-create/", views.CategoryCreateAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),
    # path("category-delete/<int:pk>/", views.CategoryDestoryAPIView.as_view()),
    # path("category-update/<int:pk>/", views.CategoryUpdateAPIView.as_view()),
    path('category', views.CategoryInfo, "category-info"),
    path('products', views.ProductView.as_view()),    # http://127.0.0.1:8000/api/products?category=id
                                                      # GET /api/products?category=id

    path('category-product-list/<int:cat_id>', views.CategoryProductList.as_view()),
    path("category/<int:id>/", views.ProductsByCategory.as_view(), name="product-category-list"),
    path('brand-product-list/<int:brand_id>', views.brand_product_list, name='brand-product-list'),
    path('products-brand', views.ProductbyBrandView.as_view()),

    path("item-list/", views.ProductListAPIView.as_view()),
]