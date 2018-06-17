from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import Conference, ConferenceManager, Reviewer, WebUser, Document, Comment, Comment


class ConferenceMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        return context


class ConferenceDetail(LoginRequiredMixin, DetailView):
    model = Conference
    context_object_name = 'conference'
    template_name = 'reviewer/conference_detail.html'

    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
    

class ConferenceEquipmentList(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'reviewer/conference_equipment_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipments'] = context['conference'].equipments.all()
        return render(request, self.template_name, context=context)

    

