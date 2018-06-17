from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.deletion import CASCADE
from django.contrib.admin.filters import ChoicesFieldListFilter
from pip.cmdoptions import editable
import uuid
from random import choice
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from _ast import Attribute


# Create your models here.
# Web 用户管理
class WebUserManager(BaseUserManager):
    def create_user(self, username, fullname, password=None):
        """
        Creates and saves a User with the given username, fullname and password.
        """
        if not username:
            raise ValueError(u'用户必须提供一个唯一的用户名')
        
        user = self.model (username = username, fullname = fullname,)        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_webadmin(self, username, fullname, password=None):
        """
        Creates and saves a User with the given username, fullname and password.
        """
        if not username:
            raise ValueError(u'用户必须提供一个唯一的用户名')
        
        user = WebAdmin.objects.create (username = username, fullname = fullname,)
        user.set_password(password)
        user.usertype = 'A'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, password):
        """
        Creates and saves a superuser with the given uaername, fullname and password.
        """
        user = self.create_webadmin(username, fullname, password)
        return user


# Web 用户
class WebUser(AbstractBaseUser):
    username = models.CharField(u'用户名', max_length=50, unique=True)
    fullname = models.CharField(u'全名', max_length=50)
       
    type_choices = (
        ('A', '系统管理员'),
        ('M', '会议管理员'),
        ('R', '审查人'),
        ('D', '设计单位'),
         )
    usertype = models.CharField(max_length=1, choices=type_choices, default='M')
           
    is_active = models.BooleanField(default=True)

    objects = WebUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname']

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        return self.usertype=='A'

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'
             

GENDER_CHOICES = (
        (u'男', u'男'),
        (u'女', u'女'),
        )

# 系统管理员
class WebAdmin(WebUser):
    gender = models.CharField(u'性别', max_length=4, blank=True, choices=GENDER_CHOICES)
    organization = models.CharField(u'工作单位', max_length=50, blank=True)
    department = models.CharField(u'部门', max_length=50, blank=True)
    title = models.CharField(u'职务/职称', max_length=20, blank=True)
    phone = models.CharField(u'电话', max_length=13, blank=True)
    memo = models.TextField(u'备注', blank=True)

    class Meta:
        verbose_name = u'系统管理员'
        verbose_name_plural = u'系统管理员'
                 
                 
# 会议管理员
class ConferenceManager(WebUser):
    gender = models.CharField(u'性别', max_length=4, blank=True, choices=GENDER_CHOICES)
    organization = models.CharField(u'工作单位', max_length=50, blank=True)
    department = models.CharField(u'部门', max_length=50, blank=True)
    title = models.CharField(u'职务/职称', max_length=20, blank=True)
    phone = models.CharField(u'电话', max_length=13, blank=True)
    memo = models.TextField(u'备注', blank=True)

    class Meta:
        verbose_name = u'会议管理员'
        verbose_name_plural = u'会议管理员'

    
# 审查专家
class Reviewer(WebUser):
    gender = models.CharField(u'性别', max_length=4, blank=True, choices=GENDER_CHOICES)
    type = models.CharField(u'类别', max_length=10, blank=True, 
                            choices=((u'主管机关',u'主管机关'),
                                     (u'军事代表',u'军事代表'),
                                     (u'承制单位',u'承制单位'),
                                     (u'承试单位',u'承试单位'),
                                     (u'使用部队',u'使用部队')))
    organization = models.CharField(u'工作单位', max_length=50, blank=True)
    department = models.CharField(u'部门', max_length=50, blank=True)
    title = models.CharField(u'职务/职称', max_length=20, blank=True)
    phone = models.CharField(u'电话', max_length=13, blank=True)
    memo = models.TextField(u'备注', blank=True)

    class Meta:
        verbose_name = u'会议代表'
        verbose_name_plural = u'会议代表'

    
# 设计单位    
class DesignOrganization(WebUser):
    shortname = models.CharField(u'简称', max_length=50, blank=True)
    address = models.CharField(u'单位地址', max_length=100, blank=True)
    contactor = models.CharField(u'联系人', max_length=20, blank=True)
    phone = models.CharField(u'联系电话', max_length=13, blank=True)
    profile = models.TextField(u'简介', blank=True)

    def get_short_name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    class Meta:
        verbose_name = u'研制单位'
        verbose_name_plural = u'研制单位'


# 设备
class Equipment(models.Model):
    ID = models.URLField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'名称', max_length=100)
    organization = models.ForeignKey(DesignOrganization, on_delete=models.CASCADE)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    last_update_time = models.DateTimeField(u'最后更新时间', auto_now=True)
    memo = models.TextField(u'备注', blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'技术设备'
        verbose_name_plural = u'技术设备'
        
        
# 技术文件
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user.short_name>/<equipment.name>/<filename>
    return '{0}/{1}/{2}'.format(instance.organization.get_short_name(), instance.equipment.name, filename)

class Document(models.Model):
    ID = models.URLField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(u'题目', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    last_update_time = models.DateTimeField(u'最后更新时间', auto_now=True)
    memo = models.TextField(u'备注', blank=True)
    file = models.FileField(u'文件', upload_to=user_directory_path, blank=True)
         
    organization = models.ForeignKey(DesignOrganization, null=True, on_delete=models.CASCADE, verbose_name='设计单位',  related_name='document_of_organization')
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.CASCADE, verbose_name='技术设备',  related_name='document_of_equipment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'技术文件'
        verbose_name_plural = u'技术文件'


class ReviewGroup(models.Model):
    ID = models.UUIDField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'名称', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'评审组'
        verbose_name_plural = u'评审组'


# 审查会议
class Conference(models.Model):
    ID = models.UUIDField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'会议名称', max_length=100)
    
    equipment_stage = models.CharField(u'研制阶段', max_length=20, blank=True,
                             choices=(
                                 (u'论证阶段',u'论证阶段'),
                                 (u'方案阶段',u'方案阶段'),
                                 (u'工程研制阶段',u'工程研制阶段'),
                                 (u'设计定型阶段',u'设计定型阶段'),
                                 (u'生产定型阶段',u'生产定型阶段')))
    review_name = models.CharField(u'评审名称', max_length=100)
    
    begin_date = models.DateTimeField(u'开始时间')
    end_date = models.DateTimeField(u'结束时间')
    address = models.CharField(u'会议地址', max_length=100)
    creator = models.ForeignKey(ConferenceManager, null=True, verbose_name =u'创建人', related_name=u'conference_creator', on_delete=models.CASCADE)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    last_updater = models.ForeignKey(ConferenceManager, null=True, verbose_name =u'最后更新人', related_name=u'conference_updater', on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(u'最后更新时间', auto_now=True)
    profile = models.TextField(u'会议须知', blank=True)
    
    managers = models.ManyToManyField(ConferenceManager, blank=True, verbose_name='会务组', related_name='manager_of')
    reviewers = models.ManyToManyField(Reviewer, blank=True, verbose_name='会议代表', related_name='reviewer_of')
    groups = models.ManyToManyField(ReviewGroup, blank=True, verbose_name='评审组', related_name='group_of')
    equipments = models.ManyToManyField(Equipment, blank=True, verbose_name='技术设备',  related_name='equipment_of')
    documents = models.ManyToManyField(Document, blank=True, verbose_name='技术文件',  related_name='document_of')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = u'审查/评审会议'
        verbose_name_plural = u'审查/评审会议'
            

class ConferenceGroupMember(models.Model):
    slug = models.SlugField(u'ID', primary_key=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name =u'审查/评审会议', related_name=u'group_set')
    group = models.ForeignKey(ReviewGroup, on_delete=models.CASCADE, verbose_name =u'评审组', related_name=u'member_set')
    member = models.ForeignKey(Reviewer, on_delete=models.CASCADE, verbose_name =u'成员', )
    role = models.CharField(u'职位', max_length=32, blank=True, choices=((u'M',u'组长'),(u'V',u'副组长'),(u'E',u'成员')))
    
                
# 专家意见    
class Comment(models.Model):
    ID = models.URLField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name='会议')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='技术设备')
    reviewer = models.ForeignKey(WebUser, on_delete=models.CASCADE, verbose_name =u'评审专家' )
    sub_time = models.DateTimeField(u'提交时间')
    last_update_time = models.DateTimeField(u'最后更新时间', auto_now=True)
    content = models.TextField(u'内容', blank=False)
    
    def __str__(self):
        return str(self.conference) + '-' + str(self.reviewer) + '(' + str(self.last_update_time) + ')'

    class Meta:
        verbose_name = u'专家意见'
        verbose_name_plural = u'专家意见'
        
    
# 评审意见
class Summary(models.Model):
    ID = models.URLField(u'ID', primary_key=True, default=uuid.uuid4, editable=False)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name='会议')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='技术设备')
    reviewer = models.ForeignKey(WebUser, on_delete=models.CASCADE, verbose_name =u'评审专家')
    sub_time = models.DateTimeField(u'提交时间')
    last_update_time = models.DateTimeField(u'最后更新时间', auto_now=True)
    content = models.TextField(u'内容')

    def __str__(self):
        return str(self.conference) + '-' + str(self.reviewer) + '(' + str(self.last_update_time) + ')'
    
    class Meta:
        verbose_name = u'评审意见'
        verbose_name_plural = u'评审意见'
        