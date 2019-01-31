from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Department
from orders.models import Order


class Ticket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                 limit_choices_to={'is_staff': False}, related_name='customers')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='users')
    subject = models.CharField(max_length=120)
    # slug = models.SlugField(editable=False)
    priority = models.CharField(max_length=120, choices=(('L', 'Low'), ('M', 'Medium'), ('H', 'High')))
    status = models.CharField(max_length=120, choices=(('O', 'Open'), ('P', 'In Progress'), ('A', 'Answered'),
                                                       ('H', 'On Hold'), ('C', 'Closed')),default='O')
    content = RichTextUploadingField(blank=True, null=True)
    attachments = models.FileField(upload_to='tickets', blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    last_replay = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('tickets:detail', kwargs={'pk': self.pk})


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    file = models.FileField(upload_to='tickets_replay', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ('created_at',)


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.subject)
#     if new_slug is not None:
#         slug = new_slug
#     queryset = Ticket.objects.filter(slug=slug).order_by("-id")
#     exists = queryset.exists()
#     if exists:
#         new_slug = '{}-{}'.format(slug, queryset.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug
#
#
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)


# Connect the generated slug function to the post model
# pre_save.connect(pre_save_post_receiver, sender=Ticket)
