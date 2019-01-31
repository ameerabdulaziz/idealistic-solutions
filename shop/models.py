from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, editable=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    is_service = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:category-product-list', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    short_description = models.CharField(max_length=250, blank=True,null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    available = models.BooleanField(default=True)
    badge = models.CharField(max_length=5, blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.slug})

    # To return discount if exsit
    @property
    def discount(self):
        if self.price_before_discount and self.price_before_discount > self.price:
            return (((self.price_before_discount - self.price) / self.price_before_discount)* -100 )
        else:
            return None


    def __str__(self):
        return '{}'.format(self.name)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    queryset = Category.objects.filter(slug=slug).order_by("-id")
    exists = queryset.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# Connect the generated slug function to the post model
pre_save.connect(pre_save_post_receiver, sender=Category)
pre_save.connect(pre_save_post_receiver, sender=Product)
