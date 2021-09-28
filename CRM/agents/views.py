from django.shortcuts import render,reverse
from leads.models import Agent
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AgentModelForm
from .mixins import OrganizerorLoginRequiredMixin
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
        agent = form.save(commit = False)
        agent.organization = self.request.user.userprofilemodel
        agent.save()
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
