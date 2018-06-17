from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import Conference, ConferenceManager, Reviewer, WebUser, Document, Comment, Comment


class DocumentMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.get(ID=self.kwargs.get('doc_id'))
        return context


def get_file_type_from_suffix (file_suffix):
    if file_suffix == 'pdf':
        return 'pdf'
    elif file_suffix == 'doc':
        return 'vnd.ms-word'
    elif file_suffix == 'docx':
        return 'vnd.openxmlformats-officedocument.wordprocessingml.document'
    else:
        return 'mime'
    
    
class DocumentOnline(LoginRequiredMixin, DocumentMixin, View):

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(Document, ID=self.kwargs.get('doc_id'))
        
        if not document.file:
            return HttpResponse('未找到文件！')
        
        with open(document.file.path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = "inline; filename=" + document.title + ".doc"
            return response


class DocumentDownload(LoginRequiredMixin, DocumentMixin, View):
    
    def get(self, request, *args, **kwargs):
        document = get_object_or_404(Document, ID=self.kwargs.get('doc_id'))
        
        if not document.file:
            return HttpResponse('未找到文件！')
        
        with open(document.file.path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = "attachment; filename=" + document.title + ".pdf"
            return response

