from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse,reverse_lazy
from django.utils import timezone


class StaticPages(models.Model):
    page_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, default=page_title,unique=True)
    content = RichTextUploadingField()
    meta_description = models.CharField(max_length=160,blank=True,null=True)
    meta_keywords = models.CharField(max_length=300,blank=True,null=True)
    meta_author = models.CharField(max_length=100,blank=True,null=True)
    active = models.BooleanField(default=False)
    created_by = models.CharField(max_length=50,blank=True,null=True)
    updated_by = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.page_title)
        super(StaticPages, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    @property
    def live(self):
        return timezone.now() >= self.published_date and self.active is True


    # This is static name that give django URL after create new record
    def get_absolute_url(self):
        return reverse('static_pages:static_pages_detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.page_title
