from django.shortcuts import render,get_object_or_404,redirect
from django.http.response import HttpResponse
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone

from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from ..models import Conference, ConferenceManager, Reviewer, ReviewGroup, Equipment
from ..forms import ManagerSelectForm, ReviewerSelectForm, GroupSelectForm, EquipmentSelectForm


class ConferenceMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        return context
    

class ConferenceRemove(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = 'manager/conference_remove.html'
    success_url = reverse_lazy('manager:conference_list')
        
    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
    
          
class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    fields = ['name', 'begin_date', 'end_date', 'address', 'profile']
    template_name = 'manager/conference_edit.html'    
    
    def get_success_url(self):
        return reverse('manager:conference:conference_detail', args=[self.kwargs['conf_id']])
    
    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
        
    def form_valid(self, form):
        form.instance.last_updater = ConferenceManager.objects.get(username=self.request.user.username)
        form.instance.last_update_time = timezone.now()
        return super().form_valid(form)
    
    
class ConferenceDetail(LoginRequiredMixin, DetailView):
    model = Conference
    context_object_name = 'conference'
    template_name = 'manager/conference_detail.html'

    def get_object(self, queryset=None):
        return Conference.objects.get(ID=self.kwargs.get('conf_id'))
    
     
class ConferenceManagerList(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_manager_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = context['conference'].managers.all()
        return render(request, self.template_name, context=context)
    
        
class ConferenceManagerDel(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        manager = ConferenceManager.objects.get(username=self.kwargs.get('username'))
        conference.managers.remove(manager)
        return redirect(reverse('manager:conference:manager_list', args=[self.kwargs['conf_id']]))

            
class ConferenceManagerAdd(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_manager_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = ConferenceManager.objects.exclude(username__in = [r.username for r in list(context['conference'].managers.all())])
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = ManagerSelectForm(context['managers'])        
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ManagerSelectForm(context['managers'], request.POST)
        
        if form.is_valid():                                            
            conference = context['conference']
            selected = form.cleaned_data.get("selected")            
            selected_managers = list(ConferenceManager.objects.filter(username__in = selected))          
            conference.managers.add(*selected_managers)
                                 
            conference.last_updater = ConferenceManager.objects.get(username=request.user.username)        
            conference.last_update_time = timezone.now()        
            conference.save()
            return redirect(reverse('manager:conference:manager_list', args=[self.kwargs['conf_id']]))
        
        context.update({'form': form})
        return render(request, self.template_name, context=context)
    

class ConferenceReviewerList(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_reviewer_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewers'] = context['conference'].reviewers.all()
        return render(request, self.template_name, context=context)
    
    
class ConferenceReviewerDel(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        manager = Reviewer.objects.get(username=self.kwargs.get('username'))
        conference.reviewers.remove(manager)
        return redirect(reverse('manager:conference:reviewer_list', args=[self.kwargs['conf_id']]))     
    
    
class ConferenceReviewerAdd(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_reviewer_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewers'] = Reviewer.objects.exclude(username__in = [r.username for r in list(context['conference'].reviewers.all())])
        return context
            
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = ReviewerSelectForm(context['reviewers'])
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ReviewerSelectForm(context['reviewers'], request.POST)
        
        if form.is_valid():                                            
            conference = context['conference']
            selected = form.cleaned_data.get("selected")            
            selected_reviewer = list(Reviewer.objects.filter(username__in = selected))          
            conference.reviewers.add(*selected_reviewer)
                                 
            conference.last_updater = ConferenceManager.objects.get(username=request.user.username)        
            conference.last_update_time = timezone.now()        
            conference.save()
            return redirect(reverse('manager:conference:reviewer_list', args=[self.kwargs['conf_id']]))
        
        context.update({'form': form})
        return render(request, self.template_name, context=context)  


class ConferenceGroupList(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_group_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = context['conference'].groups.all()
        return render(request, self.template_name, context=context)
    
    
class ConferenceGroupDel(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(ID=self.kwargs.get('conf_id'))
        group = ReviewGroup.objects.get(name=self.kwargs.get('groupname'))
        conference.groups.remove(group)
        return redirect(reverse('manager:conference:group_list', args=[self.kwargs['conf_id']]))     


class ConferenceGroupAdd(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_group_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ReviewGroup.objects.exclude(name__in = [r.name for r in list(context['conference'].groups.all())])
        return context
            
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = GroupSelectForm(context['groups'])
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = GroupSelectForm(context['groups'], request.POST)
        
        if form.is_valid():                                            
            conference = context['conference']
            selected = form.cleaned_data.get("selected")            
            selected_group = list(ReviewGroup.objects.filter(name__in = selected))          
            conference.groups.add(*selected_group)
                                 
            conference.last_updater = ConferenceManager.objects.get(username=request.user.username)        
            conference.last_update_time = timezone.now()        
            conference.save()
            return redirect(reverse('manager:conference:group_list', args=[self.kwargs['conf_id']]))
        
        context.update({'form': form})
        return render(request, self.template_name, context=context)  


    
class ConferenceEquipmentList(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_equipment_list.html'
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipments'] = context['conference'].equipments.all()
        return render(request, self.template_name, context=context)


class ConferenceEquipmentAdd(LoginRequiredMixin, ConferenceMixin, View):
    template_name = 'manager/conference_equipment_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipments'] = Equipment.objects.exclude(ID__in = [e.ID for e in list(context['conference'].equipments.all())])
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = EquipmentSelectForm(context['equipments'])        
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = EquipmentSelectForm(context['equipments'], request.POST)
        
        if form.is_valid():                                            
            conference = context['conference']
            selected = form.cleaned_data.get("selected")            
            selected_equipment = list(Equipment.objects.filter(ID__in = selected))          
            conference.equipments.add(*selected_equipment)
                                 
            conference.last_updater = ConferenceManager.objects.get(username=request.user.username)        
            conference.last_update_time = timezone.now()        
            conference.save()
            return redirect(reverse('manager:conference:equipment_list', args=[self.kwargs['conf_id']]))
        
        context.update({'form': form})
        return render(request, self.template_name, context=context) 