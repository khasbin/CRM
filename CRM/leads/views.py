from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, request
from .models import Lead, Agent, User
from .forms import LeadForm, LeadModelForm,CustomUserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizerorLoginRequiredMixin

#Create Read Update Delete + Listview

#view for signup
class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

# Create your views here.
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"



# def landing_page(request):
#     return render(request, "landing.html")


class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/lead-list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organization =user.agent.organization, agent__isnull = False)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile, agent__isnull = True)
            context.update({
                'unassigned_leads': queryset
            })
        return context
# def lead_list(request):
#     leads = Lead.objects.all()
#     context ={
#         "leads": leads
#     }
#     return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_details.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization =user.agent.organization)
            queryset = queryset.filter(agent__user = user)
        return queryset


# def lead_detail(request, pk):
#     lead = Lead.objects.get(id = pk)
#     context = {
#         "lead":lead
#     }
#     return render(request, "leads/lead_details.html", context)



class LeadCreateView(OrganizerorLoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit = False)
        lead.organization = self.request.user.userprofile
        lead.save()
        
        subject = "A new lead has been created"
        message = "Go to the crm site to view the new lead details"
        from_email = "test@test.com"
        recipient_list = ["test2@test.com"]
        send_mail(subject, message, from_email, recipient_list)
        # we want to send email whenever a lead is created 

        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print("Receiving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganizerorLoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("leads:lead-list")
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization = user.userprofile)



def lead_update(request, pk):
    lead = Lead.objects.get(id = pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance= lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form':form,
        'lead':lead
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganizerorLoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization = user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')

def lead_delete(request, pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect('/leads')

# lead = Lead.objects.get(id = pk)
#     form = LeadForm()
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect('/leads')
#     context = {
#         "lead": lead,
#         "form":form
#     }
#     return render(request, "leads/lead_update.html", context)


class AgentUpdateView(OrganizerorLoginRequiredMixin, generic.FormView):
    template_name = "leads/agent_update.html"
    form_class = None