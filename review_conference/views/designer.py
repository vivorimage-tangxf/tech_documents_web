from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import ConferenceManager, Conference, DesignOrganization, Equipment
from ..forms import PasswordForm 


class DesignerDetail(LoginRequiredMixin, DetailView):
    model = DesignOrganization
    fields = ['username', 'shortname', 'address', 'contactor', 'phone', 'profile']
    context_object_name = 'designer'
    template_name = 'designer/designer_detail.html'

    def get_object(self, queryset=None):
        return DesignOrganization.objects.get(username=self.request.user.username)


class DesignerUpdate(LoginRequiredMixin, UpdateView):
    model = DesignOrganization
    fields = ['username', 'shortname', 'address', 'contactor', 'phone', 'profile']
    template_name = 'designer/designer_edit.html'
    success_url = reverse_lazy('designer:designer_detail')

    def get_object(self, queryset=None):
        return DesignOrganization.objects.get(username=self.request.user.username)


class DesignerChangePassword(LoginRequiredMixin, FormView):
    form_class = PasswordForm
    template_name = 'designer/designer_changepassword.html'
    success_url = reverse_lazy('designer:equipment_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = form.save(request.user)
            update_session_auth_hash(request, user)  # Important!
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
 
class EquipmentList(LoginRequiredMixin, ListView):
    template_name = 'designer/equipment_list.html'
    context_object_name = 'equipments'
    
    def get_queryset(self):
        return Equipment.objects.order_by('-last_update_time')            


class EquipmentNew(LoginRequiredMixin, CreateView):
    model = Equipment
    fields = ['name', 'memo']    
    template_name = 'designer/equipment_new.html'

    def get_success_url(self):
        return reverse_lazy('designer:equipment_list')
    
    def form_valid(self, form):
        form.instance.organization = DesignOrganization.objects.get(username=self.request.user.username)
        form.instance.create_time = timezone.now()
        form.instance.last_update_time = form.instance.create_time            
        return super().form_valid(form)
       