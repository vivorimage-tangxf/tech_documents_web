from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin import AdminSite
from django.utils import timezone
from django.urls.base import reverse_lazy

# Register your models here.
from .models import WebUser, WebAdmin, ConferenceManager, Reviewer, DesignOrganization, Conference, ReviewGroup, Equipment, Document, Comment, Summary
from django.template.defaultfilters import title
from django.conf.global_settings import LOGOUT_REDIRECT_URL
    
    
class WebAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = WebAdmin
        fields = ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(WebAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.usertype = 'A'
        if commit:
            user.save()
        return user


class WebAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password  
    field with admin's password hash display field. """
    password = ReadOnlyPasswordHashField(label='密码')
     
    class Meta:
        model = WebAdmin
        fields = ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class WebAdminAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = WebAdminChangeForm
    add_form = WebAdminCreationForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'fullname', 'organization')
    list_filter = ('organization',)
    fieldsets = (
        ('基本信息', {'fields': ('username', 'password')}),
        ('个人资料', {'fields': ('fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'fullname',)
    ordering = ('username', 'fullname',)
    filter_horizontal = ()


class ConferenceManagerCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = ConferenceManager
        fields = ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ConferenceManagerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.usertype = 'M'
        if commit:
            user.save()
        return user


class ConferenceManagerChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password  
    field with admin's password hash display field. """
    password = ReadOnlyPasswordHashField(label='密码')
    
    class Meta:
        model = ConferenceManager
        fields = ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class ConferenceManagerAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = ConferenceManagerChangeForm
    add_form = ConferenceManagerCreationForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'fullname', 'organization')
    list_filter = ('organization',)
    fieldsets = (
        ('基本信息', {'fields': ('username', 'password')}),
        ('个人资料', {'fields': ('fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('username', 'fullname', 'gender', 'organization', 'department', 'title', 'phone', 'memo', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'fullname',)
    ordering = ('username', 'fullname',)
    filter_horizontal = ()


class ReviewerCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = Reviewer
        fields = ('username', 'fullname', 'gender', 'type', 'organization', 'department', 'title', 'phone', 'memo')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ReviewerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.usertype = 'R'
        if commit:
            user.save()
        return user


class ReviewerChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password  
    field with admin's password hash display field. """
    password = ReadOnlyPasswordHashField(label='密码')
    
    class Meta:
        model = Reviewer
        fields = ('username', 'fullname', 'gender', 'type', 'organization', 'department', 'title', 'phone', 'memo', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class ReviewerAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = ReviewerChangeForm
    add_form = ReviewerCreationForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'fullname', 'organization')
    list_filter = ('organization',)
    fieldsets = (
        ('基本信息', {'fields': ('username', 'password')}),
        ('个人资料', {'fields': ('fullname', 'gender', 'type', 'organization', 'department', 'title', 'phone', 'memo')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('username', 'fullname', 'gender', 'type', 'organization', 'department', 'title', 'phone', 'memo', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'fullname',)
    ordering = ('username', 'fullname',)
    filter_horizontal = ()


class DesignOrganizationCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = DesignOrganization
        fields = ('username', 'fullname', 'shortname', 'address', 'contactor', 'phone', 'profile')
            
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(DesignOrganizationCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.usertype = 'D'
        if commit:
            user.save()
        return user

class DesignOrganizationChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password  
    field with admin's password hash display field. """
    password = ReadOnlyPasswordHashField(label='密码')
    
    class Meta:
        model = DesignOrganization
        fields = ('username', 'fullname', 'shortname', 'address', 'contactor', 'phone', 'profile', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class DesignOrganizationAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = DesignOrganizationChangeForm
    add_form = DesignOrganizationCreationForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'fullname', 'shortname')
    list_filter = ('fullname',)
    fieldsets = (
        ('基本信息', {'fields': ('username', 'password')}),
        ('详细信息', {'fields': ('fullname', 'shortname', 'address', 'contactor', 'phone', 'profile')}),
    )
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('username', 'fullname', 'shortname', 'address', 'contactor', 'phone', 'profile', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'fullname',)
    ordering = ('username', 'fullname',)
    filter_horizontal = ()
    
 
class ConferenceCreationForm(forms.ModelForm):

    class Meta:
        model = Conference
        fields = ('name', 'equipment_stage', 'review_name', 'begin_date', 'end_date', 'address', 'profile', 'managers', 'reviewers', 'groups', 'equipments', 'documents')
                
    def save(self, commit=True):
        # Save the provided password in hashed format
        conf = super().save(commit=False)
        conf.create_time = timezone.now()
        if commit:
            conf.save()
        return conf
    
    
class ConferenceChangeForm(forms.ModelForm):
    
    class Meta:
        model = Conference
        fields = ('name', 'equipment_stage', 'review_name', 'begin_date', 'end_date', 'address', 'creator', 'last_updater', 'profile', 'managers', 'reviewers', 'groups', 'equipments', 'documents')

    def save(self, commit=True):
        # Save the provided password in hashed format
        conf = super().save(commit=False)
        conf.last_update_time = timezone.now()
        if commit:
            conf.save()
        return conf
       
       
class ConferenceAdmin(admin.ModelAdmin):
    form = ConferenceChangeForm
    add_form = ConferenceCreationForm
    model = Conference
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'begin_date', 'end_date', 'address')
    list_filter = ('name',)
    fieldsets = (
        ('基本信息', {'fields': ('name', 'equipment_stage', 'review_name', 'begin_date', 'end_date', 'address')}),
        ('详细信息', {'fields': ('creator', 'last_updater', 'profile')}),
        ('关联信息', {'fields': ('managers', 'reviewers', 'equipments', 'documents')}),
     )
       
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('name', 'equipment_stage', 'review_name', 'begin_date', 'end_date', 'address', 'creator', 
                   'last_updater', 'last_update_time', 'profile', 'managers', 'reviewers', 'groups', 'equipments', 'documents')}
         ),
     )
    search_fields = ('name', 'begin_date', 'address')
    ordering = ('name', 'begin_date', 'address')
    filter_horizontal = ()
    
    
class ConferenceAdminSite(AdminSite):
    site_header = '军工产品技术评审与审查会议系统-管理平台'
    

#Register your models here.#
admin_site = ConferenceAdminSite(name='Conference administration')
 
admin_site.register(WebAdmin, WebAdminAdmin)
 
admin_site.register(ConferenceManager, ConferenceManagerAdmin)
 
admin_site.register(Reviewer, ReviewerAdmin)
 
admin_site.register(DesignOrganization, DesignOrganizationAdmin)

admin_site.register(Conference, ConferenceAdmin)

admin_site.register(ReviewGroup)

admin_site.register(Equipment)

admin_site.register(Document)

admin_site.register(Comment)

admin_site.register(Summary)