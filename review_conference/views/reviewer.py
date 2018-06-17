from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Reviewer, Conference
from ..forms import PasswordForm


class ReviewerDetail(LoginRequiredMixin, DetailView):
    model = Reviewer
    context_object_name = 'reviewer'
    template_name = 'reviewer/reviewer_detail.html'

    def get_object(self, queryset=None):
        return Reviewer.objects.get(username=self.request.user.username)


class ReviewerUpdate(LoginRequiredMixin, UpdateView):
    model = Reviewer
    fields = ['username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo']
    template_name = 'reviewer/reviewer_edit.html'
    success_url = reverse_lazy('reviewer:reviewer_detail')

    def get_object(self, queryset=None):
        return Reviewer.objects.get(username=self.request.user.username)


class ReviewerChangePassword(LoginRequiredMixin, FormView):
    form_class = PasswordForm
    template_name = 'reviewer/reviewer_changepassword.html'
    success_url = reverse_lazy('reviewer:conference_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = form.save(request.user)
            update_session_auth_hash(request, user)  # Important!
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

class ReviewerConferenceList(LoginRequiredMixin, ListView):
    template_name = 'reviewer/conference_list.html'
    context_object_name = 'conferences'
    
    def get_queryset(self):
        conferences = Conference.objects.order_by('-begin_date')
        user_as_reviewer = Reviewer.objects.get(username = self.request.user.username)
        for c in conferences:
            c.can_access = user_as_reviewer in c.reviewers.all()
        return conferences

                            
          