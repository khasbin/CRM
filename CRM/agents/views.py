from django.shortcuts import render
from leads.models import Agent
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        return Agent.objects.all()