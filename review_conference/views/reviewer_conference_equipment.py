from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import Conference, ConferenceManager, Reviewer, Equipment, Document, Comment, Comment


class ConferenceEquipmentMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        context['equipment'] = Equipment.objects.get(ID=self.kwargs.get('eq_id'))
        return context


class EquipmentDetail(LoginRequiredMixin, ConferenceEquipmentMixin, DetailView):
    model = Equipment
    context_object_name = 'equipment'
    template_name = 'reviewer/equipment_detail.html'

    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
    
    
class EquipmentDocumentList(LoginRequiredMixin, ConferenceEquipmentMixin, View):
    template_name = 'reviewer/equipment_document_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = context['conference'].documents.filter(equipment = context['equipment'])
        context['documents'] = documents
        return render(request, self.template_name, context=context)

    
class EquipmentCommentDetail(LoginRequiredMixin, ConferenceEquipmentMixin, DetailView):
    model = Comment
    fields = ['reviewer', 'sub_time', 'last_update_time', 'content']
    context_object_name = 'comment'
    template_name = 'reviewer/equipment_comment_detail.html'
    
    def get_object(self, queryset=None):
        return Comment.objects.filter(conference__ID=self.kwargs.get('conf_id'), \
                                      equipment__ID=self.kwargs.get('eq_id'), \
                                      reviewer__username=self.request.user.username).first()
        

class EquipmentCommentNew(LoginRequiredMixin, ConferenceEquipmentMixin, CreateView):
    model = Comment
    fields = ['content']    
    template_name = 'reviewer/equipment_comment_edit.html'

    def get_success_url(self):
        return reverse('reviewer:conference:equipment:summary_detail', args=[self.kwargs['conf_id'], self.kwargs['eq_id']])   
    
    def form_valid(self, form):
        context = super().get_context_data(self.kwargs)
        form.instance.conference = context['conference']
        form.instance.equipment = context['equipment']
        form.instance.reviewer = Reviewer.objects.get(username=self.request.user.username)
        form.instance.sub_time = timezone.now()
        form.instance.last_update_time = form.instance.sub_time        
        return super().form_valid(form)  
    
        
class EquipmentCommentEdit(LoginRequiredMixin, ConferenceEquipmentMixin, UpdateView):
    model = Comment
    fields = ['content']
    context_object_name = 'comment'
    template_name = 'reviewer/equipment_comment_edit.html'
        
    def get_object(self, queryset=None):
        return Comment.objects.get(ID = self.kwargs['cmt_id'])

    def get_success_url(self):
        return reverse('reviewer:conference:equipment:comment_detail', args=[self.kwargs['conf_id'], self.kwargs['eq_id']])
    
    def form_valid(self, form):
        form.instance.last_update_time = timezone.now()
        return super().form_valid(form)

