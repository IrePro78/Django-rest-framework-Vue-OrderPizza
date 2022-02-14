from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    @staticmethod
    def make_thumbnail(image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Variant(models.Model):
    SIZES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Giant', 'Giant'),
        ('0.3 L', '0.3 L'),
        ('0.5 L', '0.5 L'),
        ('1.0 L', '1.0 L'),
    )
    size = models.CharField(max_length=20, choices=SIZES, default='Medium')
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ('size',)

    def __str__(self):
        return self.size


class Topping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Sauce(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, related_name='items', on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ('variant',)

    def __str__(self):
        return f'{self.product} {self.variant} {self.price}'


class ProductVariantTopping(models.Model):
    product_variant = models.ForeignKey(ProductVariant, related_name='items', on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, related_name='items', blank=True)
    sauces = models.ManyToManyField(Sauce, related_name='items', blank=True)

    def __str__(self):
        return '%s' % self.id
