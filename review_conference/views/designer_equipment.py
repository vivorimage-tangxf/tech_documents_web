from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import DesignOrganization, Equipment, Document, Summary


class EquipmentMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = Equipment.objects.get(ID=self.kwargs.get('eq_id'))
        return context


class EquipmentDetail(LoginRequiredMixin, DetailView):
    model = Equipment
    context_object_name = 'equipment'
    template_name = 'designer/equipment_detail.html'

    def get_object(self, queryset=None):
        return Equipment.objects.get(ID=self.kwargs.get('eq_id'))
    

class EquipmentUpdate(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ['memo']
    template_name = 'designer/equipment_edit.html'    
    
    def get_object(self, queryset=None):
        return Equipment.objects.get(ID=self.kwargs.get('eq_id'))
    
    def get_success_url(self):
        return reverse('designer:equipment:equipment_detail', args=[self.kwargs.get('eq_id')])
    
    def form_valid(self, form):
        form.instance.last_update_time = timezone.now()
        return super(EquipmentUpdate, self).form_valid(form)
      
      
class EquipmentRemove(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'designer/equipment_remove.html'
    success_url = reverse_lazy('designer:equipment_list')
        
    def get_object(self, queryset=None):
        return Equipment.objects.get(ID=self.kwargs.get('eq_id'))
    

class EquipmentDocumentList(LoginRequiredMixin, EquipmentMixin, View):
    template_name = 'designer/equipment_document_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.filter(equipment = context['equipment'])
        return render(request, self.template_name, context=context)

    
class EquipmentDocumentNew(LoginRequiredMixin, EquipmentMixin, CreateView):
    model = Document
    fields = ['title', 'memo', 'file']    
    template_name = 'designer/equipment_document_new.html'

    def get_success_url(self):
        return reverse('designer:equipment:document_list', args=[self.kwargs['eq_id']])   
    
    def form_valid(self, form):
        context = super().get_context_data(**self.kwargs)
        form.instance.organization = DesignOrganization.objects.get(username=self.request.user.username)
        form.instance.equipment = context['equipment']
        form.instance.create_time = timezone.now()
        form.instance.last_update_time = form.instance.create_time
        return super().form_valid(form)        
        
            
class EquipmentDocumentDel(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        document = Document.objects.get(ID=self.kwargs.get('doc_id'))
        document.file.delete()
        document.delete()
        return redirect(reverse('designer:equipment:document_list', args=[self.kwargs['eq_id']]))    
    

class EquipmentDocumentUpdate(LoginRequiredMixin, EquipmentMixin, UpdateView):
    model = Document
    fields = ['title', 'memo', 'file']
    template_name = 'designer/equipment_document_edit.html'    
    
    def get_object(self, queryset=None):
        return Document.objects.get(ID=self.kwargs.get('doc_id'))
    
    def get_success_url(self):
        return reverse_lazy('designer:equipment:document_list', args=[self.kwargs.get('eq_id')])
    
    def form_valid(self, form):
        form.instance.last_update_time = timezone.now()
        return super().form_valid(form)
    

class EquipmentSummaryList(LoginRequiredMixin, EquipmentMixin, View):
    template_name = 'designer/equipment_summary_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summaries'] = Summary.objects.filter(equipment = context['equipment'])
        return render(request, self.template_name, context=context)    
        