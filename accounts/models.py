from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=120)
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    supervisor_id = models.CharField(max_length=300, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='userprofile')
    slug = models.SlugField(unique=True, editable=False)
    type = models.CharField(max_length=1, choices=(('C', 'Customer'), ('S', 'Staff')), blank=True, null=True)
    image = models.ImageField(upload_to='avatar', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    zip = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """Auto generate the slug field from the username of users"""
        self.slug = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Create a link to to view detail for each object in the post model"""
        return reverse('accounts:detail', kwargs={'slug': self.slug})


# Auto create user profile when a new user is added
def create_profile(sender, **kwargs):
    if kwargs['created']:

        UserProfile.objects.create(user=kwargs['instance'],type = 'C')
        # Customer should not be staff
        # Staff.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


# email must be unique in register
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
