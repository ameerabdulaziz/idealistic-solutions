from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import Staff
from orders.models import OrderItem
from .forms import ReplayForm, TicketForm
from .models import Ticket, Reply

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'ticketing_system/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        # If the user is superuser, he allows to see all tickets
        if self.request.user.is_superuser:
            print('super')
            return Ticket.objects.all()
        elif not self.request.user.is_staff:
            print('customer')
            return Ticket.objects.filter(customer=self.request.user)
        else:
            # If the user is agent, he allows to see the tickets that assigned to him
            if self.request.user.staff.role.name == 'agent':
                print('agent')
                return Ticket.objects.filter(assigned_to=self.request.user)
            # If the user is supervisor, he allows to see the tickets that assigned to him and assigned to the agents
            # that he supervise them
            elif self.request.user.staff.role.name == 'supervisor':
                # staffs = list(Staff.objects.all().values_list('supervisor_id', flat=True))
                # agents_ids = []
                # for staff in users_ids:
                #     if staff is not None:
                #         agents_ids += (staff.split(','))
                # print(agents_ids)
                print('supervisor')
                tickets = Ticket.objects.filter(assigned_to=self.request.user)

                agents = Staff.objects.filter(supervisor_id__contains=self.request.user.id)

                agents_ids = []
                for agent in agents:
                    agents_ids.append(agent.user_id)
                for agent_id in agents_ids:

                    tickets = tickets | Ticket.objects.filter(assigned_to=agent_id)

                return tickets
            # If the user is manager, he allows to see the tickets that assigned to him and assigned to the agents
            # that he supervise them
            elif self.request.user.staff.role.name == 'Manager':
                print('manager')
                tickets = Ticket.objects.filter(assigned_to=self.request.user)

                supervisors = Staff.objects.filter(supervisor_id__contains=self.request.user.id)
                supervisors_ids = []
                for supervisor in supervisors:
                    supervisors_ids.append(supervisor.user_id)
                for supervisor_id in supervisors_ids:
                    print(supervisor_id)
                    tickets = tickets | Ticket.objects.filter(assigned_to=supervisor_id)
                    agents = Staff.objects.filter(supervisor_id__contains=supervisor_id)
                    print(agents)
                    agents_ids = []
                    for agent in agents:
                        agents_ids.append(agent.user_id)
                    for agent_id in agents_ids:
                        print(agent_id)
                        tickets = tickets | Ticket.objects.filter(assigned_to=agent_id)
                return tickets


class TicketDetail(LoginRequiredMixin,generic.DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.get_object().order)

        context['form'] = ReplayForm
        return context


class TicketCreateView(LoginRequiredMixin,generic.CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')


    def get_form_kwargs(self):
        kw = super(TicketCreateView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.customer = self.request.user
        instance.save()
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')

    def get_form_kwargs(self):
        kw = super(TicketUpdateView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw


class TicketDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets:list')


class ReplayCreateView(LoginRequiredMixin,generic.CreateView):
    model = Reply
    form_class = ReplayForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tickets:detail', kwargs={'pk': self.kwargs['pk']})

def TicketreopenView(request,pk):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        user = request.user
        ticket_id = request.POST['ticket_id']
        ticket_details = Ticket.objects.get(pk=ticket_id)
        if user == ticket_details.customer:
            ticket_details.status = 'O'
            ticket_details.save()
            new_link = "/tickets/" + str(ticket_id)+"/"
            return redirect('tickets:detail', pk=ticket_id)

        else:
            raise Http404

    return redirect('tickets:list')


def TicketcloseView(request,pk):

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        user = request.user
        ticket_id = request.POST['ticket_id']
        ticket_details = Ticket.objects.get(pk=ticket_id)
        if user == ticket_details.customer:
            ticket_details.status = 'C'
            ticket_details.save()
            new_link = "/tickets/" + str(ticket_id)+"/"
            return redirect('tickets:detail', pk=ticket_id)

        else:
            raise Http404

    return redirect('tickets:list')
