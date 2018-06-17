from django import forms
from .models import ConferenceManager, Conference, Summary
    

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=30)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
        
    def set_errors(self,content):   
        if content and len(content)>0:   
            errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())  
            errors.append(content)  


class PasswordForm(forms.Form):    
    oldpassword = forms.CharField(label='原密码', widget=forms.PasswordInput)
    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='新密码确认', widget=forms.PasswordInput)
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2
    
    def save(self, user, commit=True):
        # Save the provided password in hashed format
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

        
class ManagerForm(forms.ModelForm):

    class Meta:
        model=ConferenceManager
        fields=('fullname','gender','organization','department','title','phone','memo')

       
class ConferenceCreationForm(forms.ModelForm):

    class Meta:
        model = Conference
        fields = ('name', 'begin_date', 'end_date', 'address', 'profile')
                
    def save(self, commit=True):
        # Save the provided password in hashed format
        conf = super(ConferenceCreationForm, self).save(commit=False)
        conf.creator = self.request.user
        conf.create_time = now()
        if commit:
            conf.save()
        return conf       
    
    
class ConferenceChangeForm(forms.ModelForm):
    
    class Meta:
        model = Conference
        fields = ('name', 'begin_date', 'end_date', 'address', 'creator', 'last_updater', 'profile')

    def save(self, commit=True):
        # Save the provided password in hashed format
        conf = super(ConferenceChangeForm, self).save(commit=False)
        conf.last_updater = self.request.user
        conf.last_update_time = now()
        if commit:
            conf.save()
        return conf    
    

class ManagerSelectForm(forms.Form):
    selected = forms.MultipleChoiceField(label='会议管理员', widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, managers, *args, **kwargs):
        super(ManagerSelectForm, self).__init__(*args, **kwargs)
        self.fields['selected'].choices = ((m.username, m.fullname+'('+m.username+')') for m in managers)


class ReviewerSelectForm(forms.Form):
    selected = forms.MultipleChoiceField(label='审查人', widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, reviewers, *args, **kwargs):
        super(ReviewerSelectForm, self).__init__(*args, **kwargs)
        self.fields['selected'].choices = ((r.username, r.fullname+'('+r.username+')') for r in reviewers)

       
class GroupSelectForm(forms.Form):
    selected = forms.MultipleChoiceField(label='审查组', widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, groups, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected'].choices = ((r.name, r.name) for r in groups)
       
       
class EquipmentSelectForm(forms.Form):
    selected = forms.MultipleChoiceField(label='技术设备', widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, reviewers, *args, **kwargs):
        super(EquipmentSelectForm, self).__init__(*args, **kwargs)
        self.fields['selected'].choices = ((r.ID, r.name+'('+r.organization.shortname+')') for r in reviewers)


class DocumentSelectForm(forms.Form):
    selected = forms.MultipleChoiceField(label='技术文件', widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, documents, *args, **kwargs):
        super(DocumentSelectForm, self).__init__(*args, **kwargs)
        self.fields['selected'].choices = ((d.ID, d.title) for d in documents)
 
 
class ConferenceSummaryForm(forms.ModelForm):

    class Meta:
        model = Summary
        fields = ('content',)
      
      