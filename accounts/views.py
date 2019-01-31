from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from idealisticsolutions.settings import EMAIL_HOST_USER

from .models import UserProfile
from .forms import UserForm, UserProfileForm, RegisterForm
from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            send_mail(
                'Registration Message',
                'Thanks for join our site',
                EMAIL_HOST_USER,
                [form.cleaned_data.get('email'), EMAIL_HOST_USER],
                fail_silently=False,
                )
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form_register': form})


class UserDetailView(generic.DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = Order.objects.filter(emailAddress=self.request.user.email)
        return context


def user_edit_view(request, slug):
    query_set = get_object_or_404(UserProfile, slug=slug)
    user_form = UserForm(request.POST or None, instance=query_set.user)
    user_profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=query_set)

    # Declare session['previous_url'] for once and delete it after post process
    if 'previous_url' not in request.session:
        request.session['previous_url'] = request.META.get('HTTP_REFERER')
    if user_form.is_valid() and user_profile_form.is_valid():
        user_form.save()
        user_profile_form.save()
        previous_url = request.session['previous_url']  # Save the session before the deletion
        del request.session['previous_url']
        return redirect(previous_url)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'accounts/userprofile_form.html', context)
