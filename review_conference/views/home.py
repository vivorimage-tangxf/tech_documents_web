from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect  
from django.core.urlresolvers import reverse

from django.views.generic import View
from ..forms import LoginForm

class Welcome(View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        user = request.user

        if not user.is_anonymous() and user.is_authenticated:
            if user.usertype=='M':                
                return HttpResponseRedirect(reverse('manager:conference_list'))
            elif user.usertype=='R':
                return HttpResponseRedirect(reverse('reviewer:conference_list'))
            elif user.usertype=='D':
                return HttpResponseRedirect(reverse('designer:equipment_list'))
            elif user.usertype=='A':
                return HttpResponseRedirect(reverse('admin:index'))                
            else:
                form.set_errors("未知的用户类型")

        return render(request, self.template_name, {'form':form})
        
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        user = request.user
                
        if form.is_valid():                
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            
            user = auth.authenticate(username = username, password = password)      
            if user is not None:
                auth.login(request, user)
                if user.usertype=='M':                
                    print (user.username, user.usertype)
                    return HttpResponseRedirect(reverse('manager:conference_list'))
                elif user.usertype=='R':
                    print (user.username, user.usertype)
                    return HttpResponseRedirect(reverse('reviewer:conference_list'))
                elif user.usertype=='D':
                    return HttpResponseRedirect(reverse('designer:equipment_list'))                
                elif user.usertype=='A':
                    return HttpResponseRedirect(reverse('admin:index'))                
                else:
                    form.set_errors("未知的用户类型")
            else:
                form.set_errors(u"未知用户") 
                    
        return render(request, self.template_name, {'form':form})            

