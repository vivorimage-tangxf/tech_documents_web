from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import Conference, ConferenceManager, Equipment, Document, Comment, Summary
from ..forms import DocumentSelectForm


class ConferenceEquipmentMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        context['equipment'] = Equipment.objects.get(ID=self.kwargs.get('eq_id'))
        return context


class EquipmentDel(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        equipment = Equipment.objects.get(ID=self.kwargs.get('eq_id'))
        conference.equipments.remove(equipment)
        return redirect(reverse('manager:conference:equipment_list', args=[self.kwargs['conf_id']]))    


class EquipmentDetail(LoginRequiredMixin, ConferenceEquipmentMixin, DetailView):
    model = Equipment
    context_object_name = 'equipment'
    template_name = 'manager/conference_equipment_detail.html'

    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
    
    
class EquipmentDocumentList(LoginRequiredMixin, ConferenceEquipmentMixin, View):
    template_name = 'manager/equipment_document_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = context['conference'].documents.filter(equipment = context['equipment'])
        context['documents'] = documents
        return render(request, self.template_name, context=context)
    
    
class EquipmentDocumentDel(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        document = Document.objects.get(ID=self.kwargs.get('doc_id'))
        conference.documents.remove(document)
        return redirect(reverse('manager:conference:equipment:document_list', args=[self.kwargs['conf_id'],self.kwargs['eq_id']]))    
    
    
class EquipmentDocumentAdd(LoginRequiredMixin, ConferenceEquipmentMixin, View):
    template_name = 'manager/equipment_document_add.html'
    
    def get_context(self, **kwargs):
        context = super().get_context_data()
        context['documents'] = Document.objects.filter(equipment = context['equipment']).exclude(ID__in = [d.ID for d in list(context['conference'].documents.all())])
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context(**kwargs)
        context['form'] = DocumentSelectForm(context['documents'])
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context(**kwargs)
        form = DocumentSelectForm(context['documents'], request.POST)
        
        if form.is_valid():                                            
            conference = context['conference']
            selected = form.cleaned_data.get("selected")            
            selected_document = list(Document.objects.filter(ID__in = selected))          
            conference.documents.add(*selected_document)
                                 
            conference.last_updater = ConferenceManager.objects.get(username=request.user.username)        
            conference.last_update_time = timezone.now()        
            conference.save()
            return redirect(reverse('manager:conference:equipment:document_list', args=[self.kwargs['conf_id'],self.kwargs['eq_id']]))
        
        context.update({'form': form})
        return render(request, self.template_name, context=context)      
    

class EquipmentCommentList(LoginRequiredMixin, ConferenceEquipmentMixin, View):
    template_name = 'manager/equipment_comment_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(conference=context['conference'], equipment=context['equipment'])
        return render(request, self.template_name, context=context)    

    
class EquipmentSummaryDetail(LoginRequiredMixin, ConferenceEquipmentMixin, DetailView):
    model = Summary
    fields = ['reviewer', 'sub_time', 'last_update_time', 'content']
    context_object_name = 'summary'
    template_name = 'manager/equipment_summary_detail.html'
    
    def get_object(self, queryset=None):
        return Summary.objects.filter(conference__ID=self.kwargs.get('conf_id'), equipment__ID=self.kwargs.get('eq_id')).first()
        

class EquipmentSummaryNew(LoginRequiredMixin, ConferenceEquipmentMixin, CreateView):
    model = Summary
    fields = ['content']    
    template_name = 'manager/equipment_summary_edit.html'

    def get_success_url(self):
        return reverse('manager:conference:equipment:summary_detail', args=[self.kwargs['conf_id'], self.kwargs['eq_id']])   
    
    def form_valid(self, form):
        context = super().get_context_data(self.kwargs)
        form.instance.conference = context['conference']
        form.instance.equipment = context['equipment']
        form.instance.reviewer = ConferenceManager.objects.get(username=self.request.user.username)
        form.instance.sub_time = timezone.now()
        form.instance.last_update_time = form.instance.sub_time        
        return super().form_valid(form)  
    
        
class EquipmentSummaryEdit(LoginRequiredMixin, ConferenceEquipmentMixin, UpdateView):
    model = Summary
    fields = ['content']
    context_object_name = 'summary'
    template_name = 'manager/equipment_summary_edit.html'
        
    def get_object(self, queryset=None):
        return Summary.objects.get(ID = self.kwargs['smr_id'])

    def get_success_url(self):
        return reverse('manager:conference:equipment:summary_detail', args=[self.kwargs['conf_id'], self.kwargs['eq_id']])
    
    def form_valid(self, form):
        form.instance.last_update_time = timezone.now()
        return super().form_valid(form)

