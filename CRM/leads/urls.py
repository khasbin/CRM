from leads.models import Lead
from django.urls import path
from .views import LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AgentUpdateView

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name = 'lead-list'),
    path('<int:pk>/',LeadDetailView.as_view(),name = 'lead-detail'),
    path('create/',LeadCreateView.as_view(), name = 'lead-create'),
    path('<int:pk>/update/',LeadUpdateView.as_view(), name = 'lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name = 'lead-delete'),
    path('<int:pk>/agent-update/',AgentUpdateView.as_view(), name = "agent-update"),
]
