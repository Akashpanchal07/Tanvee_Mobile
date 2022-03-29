from django.urls import include, path

app_name = "common_urls"
urlpatterns = [
    path("", include(("common.urls"))),
    path("", include(('products.urls'))),
    # path("", include(('order.urls')))
    # path("", include(('stock_mg.urls'))),
    # path("", include(('inventory_manage.urls'))),
]