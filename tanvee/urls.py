"""tanvee URL Configuration
"""
from django.contrib import admin
from django.urls import path, include


# Dajngo Admin Customization
admin.site.site_title = " Tanvee Mobile Admin "
admin.site.site_header = " Tanvee Admin Site"
admin.site.index_title = " Tanvee Mobile Admin "

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("common.app_urls", namespace="common_urls")),
]
