from django.shortcuts import render,reverse
from leads.models import Agent
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AgentModelForm
from .mixins import OrganizerorLoginRequiredMixin
from  django.core.mail import send_mail
import random
# Create your views here.

class AgentListView(OrganizerorLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        orgs = self.request.user.userprofilemodel
        return Agent.objects.filter(organization = orgs)


class AgentCreateView(OrganizerorLoginRequiredMixin, generic.CreateView):
    template_name  ='agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_organizer = False
        user.save()
        user.set_password(f"{random.randint(0,100000)}")
        Agent.objects.create(user = user, organization = self.request.user.userprofilemodel)

        send_mail(
            subject= "Invited as an agent",
            message = "You are invited as an agent. Please login to start working as an agent", 
            from_email="master@mail.com",
            recipient_list=[user.email]       
        )
        # agent.organization = self.request.user.userprofilemodel
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganizerorLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_details.html'
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganizerorLoginRequiredMixin, generic.UpdateView):
    template_name  ='agents/agent_update.html'
    context_object_name = "agent"
    form_class = AgentModelForm

    def get_queryset(self):
        return Agent.objects.all()

    def get_success_url(self):
        return reverse('agents:agent-list')

class AgentDeleteView(OrganizerorLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse('agents:agent-list')
        
    def get_queryset(self):
        return Agent.objects.all()
