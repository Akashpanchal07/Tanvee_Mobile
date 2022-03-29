from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.conf import settings
from common.models import User, TimeStampMixin
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from products.utils import availability_choice, soft_delete

# Category Model
class Category(TimeStampMixin):
    name = models.CharField(
        "Category Name", max_length=250, null=False,
        blank=False, unique=True)
    categoryImage = models.ImageField(
        "Category Image", upload_to='static/product_module/category',
        null=False, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def image_tag(self):
        try:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.categoryImage.url))
        except Exception as e:
            print(e)

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Category.
        """
        return reverse('category-detail-view', args=[str(self.id)])

# Brand Model for Product
class Brand(TimeStampMixin):
    name = models.CharField("Brand Name", max_length=255, null=False, blank=False)

    class Meta:

        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Brand.
        """
        return reverse('brand-detail-view', args=[str(self.id)])


'''
# Tag Model for Product
class Tags(TimeStampMixin):
    tag = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name_plural = "Tags"
'''

# Size model for ProductSize
class Size(TimeStampMixin):
    size = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.size

    def save(self, *args, **kwargs):
        self.size = self.size.lower()
        super(Size, self).save(*args, **kwargs)


# Unit of Measure
class UnitofMeasure(TimeStampMixin):
    name = models.CharField("Unit of Measure", max_length=50, blank=True, null=True)
    short_name = models.CharField("UoM", max_length=5, blank=True, null=True)

    class Meta:
        verbose_name = 'Unit of Measure'
        verbose_name_plural = 'Unit of Measures'

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Unit of Measure.
        """
        return reverse('uom-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.short_name


class ProductManager(models.Manager):
    def get_queryset(self):
        if not settings.DISPLAY_OUT_OF_STOCK_PRODUCTS:
            return super().get_queryset().filter(soft_delete=False, status=True)
        return super().get_queryset().filter(soft_delete=False)


# Product Model
class Product(TimeStampMixin):
    name = models.CharField(max_length=255, null=False, blank=False)

    short_description = RichTextField(
        help_text="Not more than 30 words.", blank=True, null=True)
    description = RichTextField(
        help_text="Bio e.g. size, material type, etc", blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name="category_product", on_delete=models.CASCADE, default=None, blank=True)
    '''quantity_left = models.BigIntegerField(
        null=True, blank=True, default=0,
        help_text="Automatic quantity decreased after order placed. 
        Leave it empty for unlimited/manual quantity of the product.")'''
    status = models.BooleanField(choices=availability_choice, null=False, blank=False,
                                 default=True, help_text="Status with Available are only visible in the site.")
    sizes = models.ForeignKey(Size, on_delete=models.CASCADE, default=None, blank=True)
    brand_name = models.ForeignKey(
        Brand, related_name='brand', blank=True, null=True, on_delete=models.CASCADE)
    uom = models.ForeignKey(UnitofMeasure, on_delete=models.CASCADE, blank=True, null=True)
    '''tags = models.ManyToManyField(
        Tags, related_name="product_tags", blank=True) '''
    price = models.FloatField(max_length=100, null=False, blank=False)
    '''related_products = models.ManyToManyField(
        'self', blank=True, related_name='related_products')'''
    main_image = models.ImageField(
        upload_to='static/product_module/product', help_text=("Upload a product image"), blank=True
    )
    soft_delete = models.BooleanField(
        choices=soft_delete, null=False, blank=False, default=False)

    objects = ProductManager()
    deletedObject = models.Manager()

    """if settings.MULTI_VENDOR:
        vendor = models.ForeignKey(
            'Vendor.Vendor', on_delete=models.CASCADE, null=False, blank=False)

    if settings.HAS_OFFER_APP:
        offers = models.ManyToManyField(
            "Offer.OfferCategory", related_name="offer_products", blank=True)"""

    def __str__(self):
        return self.name

    def delete_softly(self):
        self.soft_delete = not self.soft_delete

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('product-detail-view', args=[str(self.id)])

    '''def get_category(self):
        return "\n".join([p.category.name for p in self.category.all()])

    def get_sizes(self):
        return "\n".join([p.sizes.size for p in self.sizes.all()])'''


# Models for Products Images
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/product_module/product', help_text=("Upload a product image"), blank=True)

    def __str__(self):
        return str(self.product.name)

    def image_tag(self):
        try:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
        except Exception as e:
            pass

    image_tag.short_description = 'Image'
