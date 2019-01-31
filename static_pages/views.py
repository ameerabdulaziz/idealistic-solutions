from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from static_pages.models import StaticPages
from static_pages.forms import StaticPageForm
from django.db.models import Q


class StaticPagesCreateView(LoginRequiredMixin,generic.CreateView):
    model = StaticPages
    REDIRECT_FIELD_NAME = 'static_pages:static_pages_detail'
    form_class = StaticPageForm


class StaticPagesupdateView(LoginRequiredMixin,generic.UpdateView):
    model = StaticPages
    form_class = StaticPageForm


class StaticPagesListView(LoginRequiredMixin,generic.ListView):
    model = StaticPages
    paginate_by = 20
    def get_queryset(self):
        return StaticPages.objects.all().order_by('page_title')


class StaticPagesDetailView(generic.DetailView):
    model = StaticPages

    # Disaple below command to be able to see page even it's not active,
    # In this case will be appeared only to super user
    # def get_queryset(self):
        # return StaticPages.objects.filter(published_date__lte=timezone.now(),active=True)


class StaticPagesDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = StaticPages
    success_url = reverse_lazy('static_pages:static_pages_list')
