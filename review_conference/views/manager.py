from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import ConferenceManager, Conference
from ..forms import PasswordForm


class ManagerDetail(LoginRequiredMixin, DetailView):
    model = ConferenceManager
    context_object_name = 'manager'
    template_name = 'manager/manager_detail.html'

    def get_object(self, queryset=None):
        return ConferenceManager.objects.get(username=self.request.user.username)


class ManagerUpdate(LoginRequiredMixin, UpdateView):
    model = ConferenceManager
    fields = ['username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo']
    template_name = 'manager/manager_edit.html'
    success_url = reverse_lazy('manager:manager_detail')

    def get_object(self, queryset=None):
        return ConferenceManager.objects.get(username=self.request.user.username)


class ManagerChangePassword(LoginRequiredMixin, FormView):
    form_class = PasswordForm
    template_name = 'manager/manager_changepassword.html'
    success_url = reverse_lazy('manager:conference_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = form.save(request.user)
            update_session_auth_hash(request, user)  # Important!
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
      
        
class ManagerConferenceList(LoginRequiredMixin, ListView):
    template_name = 'manager/conference_list.html'
    context_object_name = 'conferences'
    
    def get_queryset(self):
        conferences = Conference.objects.order_by('-begin_date')
        user_as_manager = ConferenceManager.objects.get(username = self.request.user.username)
        for c in conferences:
            c.can_access = user_as_manager==c.creator or user_as_manager in c.managers.all()
        return conferences


class ManagerConferenceNew(LoginRequiredMixin, CreateView):
    model = Conference
    fields = ['name', 'equipment_stage', 'begin_date', 'end_date', 'address', 'profile']    
    template_name = 'manager/conference_new.html'
    success_url = reverse_lazy('manager:conference_list')
    
    def form_valid(self, form):
        form.instance.creator = ConferenceManager.objects.get(username=self.request.user.username)
        form.instance.create_time = timezone.now()
        form.instance.last_updater = form.instance.creator
        form.instance.last_update_time = form.instance.create_time            
        return super().form_valid(form)
