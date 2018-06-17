from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .admin import admin_site
from . import views


# for Designer
designer_equipment_patterns = ([    
    url(r'^$', views.designer_equipment.EquipmentDetail.as_view(), name="equipment_detail"),
    url(r'^edit/$', views.designer_equipment.EquipmentUpdate.as_view(), name="equipment_edit"),
    url(r'^remove/$', views.designer_equipment.EquipmentRemove.as_view(), name="equipment_remove"),

    url(r'^documents/$', views.designer_equipment.EquipmentDocumentList.as_view(), name="document_list"),
    url(r'^document/add/$', views.designer_equipment.EquipmentDocumentNew.as_view(), name="document_add"),
    url(r'^document/(?P<doc_id>[^/]+)/remove/$', views.designer_equipment.EquipmentDocumentDel.as_view(), name="document_remove"),
    url(r'^document/(?P<doc_id>[^/]+)/edit/$', views.designer_equipment.EquipmentDocumentUpdate.as_view(), name="document_edit"),

    url(r'^summaries/$', views.designer_equipment.EquipmentSummaryList.as_view(), name="summary_list"),
    ], 'equipment')

designer_patterns = ([
    url(r'^detail/$', views.designer.DesignerDetail.as_view(), name="designer_detail"),
    url(r'^edit/$', views.designer.DesignerUpdate.as_view(), name="designer_edit"),
    url(r'^cpw/$', views.designer.DesignerChangePassword.as_view(), name="designer_cpw"),

    url(r'^equipments/$', views.designer.EquipmentList.as_view(), name="equipment_list"),
    url(r'^equipment/new/$', views.designer.EquipmentNew.as_view(), name="equipment_new"),
    url(r'^equipment/(?P<eq_id>[^/]+)/', include(designer_equipment_patterns)),    
    ], 'designer')



# for Manager
manager_conference_equipment_patterns = ([    
    url(r'^$', views.manager_conference_equipment.EquipmentDetail.as_view(), name="equipment_detail"),
    url(r'^remove/$', views.manager_conference_equipment.EquipmentDel.as_view(), name="equipment_remove"),

    url(r'^documents/$', views.manager_conference_equipment.EquipmentDocumentList.as_view(), name="document_list"),
    url(r'^document/add/$', views.manager_conference_equipment.EquipmentDocumentAdd.as_view(), name="document_add"),
    url(r'^document/(?P<doc_id>[^/]+)/remove/$', views.manager_conference_equipment.EquipmentDocumentDel.as_view(), name="document_remove"),

    url(r'^comments/$', views.manager_conference_equipment.EquipmentCommentList.as_view(), name="comment_list"),
    
    url(r'^summary/$', views.manager_conference_equipment.EquipmentSummaryDetail.as_view(), name="summary_detail"),
    url(r'^summary/new/$', views.manager_conference_equipment.EquipmentSummaryNew.as_view(), name="summary_new"),
    url(r'^summary/(?P<smr_id>[^/]+)/edit/$', views.manager_conference_equipment.EquipmentSummaryEdit.as_view(), name="summary_edit"),
    ], 'equipment')

manager_conference_patterns = ([
    url(r'^$', views.manager_conference.ConferenceDetail.as_view(), name="conference_detail"),
    url(r'^edit/$', views.manager_conference.ConferenceUpdate.as_view(), name="conference_edit"),
    url(r'^remove/$', views.manager_conference.ConferenceRemove.as_view(), name="conference_remove"),

    url(r'^managers/$', views.manager_conference.ConferenceManagerList.as_view(), name="manager_list"),
    url(r'^manager/add/$', views.manager_conference.ConferenceManagerAdd.as_view(), name="manager_add"),
    url(r'^manager/(?P<username>[^/]+)/remove/$', views.manager_conference.ConferenceManagerDel.as_view(), name="manager_remove"),
    
    url(r'^reviewers/$', views.manager_conference.ConferenceReviewerList.as_view(), name="reviewer_list"),
    url(r'^reviewer/add/$', views.manager_conference.ConferenceReviewerAdd.as_view(), name="reviewer_add"),
    url(r'^reviewer/(?P<username>[^/]+)/remove/$', views.manager_conference.ConferenceReviewerDel.as_view(), name="reviewer_remove"),
    
    url(r'^groups/$', views.manager_conference.ConferenceGroupList.as_view(), name="group_list"),
    url(r'^group/add/$', views.manager_conference.ConferenceGroupAdd.as_view(), name="group_add"),
    url(r'^group/(?P<groupname>[^/]+)/remove/$', views.manager_conference.ConferenceGroupDel.as_view(), name="group_remove"),
    
    url(r'^equipments/$', views.manager_conference.ConferenceEquipmentList.as_view(), name="equipment_list"),
    url(r'^equipments/add/$', views.manager_conference.ConferenceEquipmentAdd.as_view(), name="equipment_add"),
    url(r'^equipment/(?P<eq_id>[^/]+)/', include(manager_conference_equipment_patterns)),    
    ], 'conference')

manager_patterns = ([
    url(r'^detail/$', views.manager.ManagerDetail.as_view(), name="manager_detail"),
    url(r'^edit/$', views.manager.ManagerUpdate.as_view(), name="manager_edit"),
    url(r'^cpw/$', views.manager.ManagerChangePassword.as_view(), name="manager_cpw"),

    url(r'^conferences/$', views.manager.ManagerConferenceList.as_view(), name="conference_list"),
    url(r'^conference/new/$', views.manager.ManagerConferenceNew.as_view(), name="conference_new"),
    url(r'^conference/(?P<conf_id>[^/]+)/', include(manager_conference_patterns)),    
    ], 'manager')
    


# for Reviewer
reviewer_conference_equipment_patterns = ([    
    url(r'^$', views.reviewer_conference_equipment.EquipmentDetail.as_view(), name="equipment_detail"),
    url(r'^documents/$', views.reviewer_conference_equipment.EquipmentDocumentList.as_view(), name="document_list"),
    url(r'^comment/$', views.reviewer_conference_equipment.EquipmentCommentDetail.as_view(), name="comment_detail"),
    url(r'^comment/new/$', views.reviewer_conference_equipment.EquipmentCommentNew.as_view(), name="comment_new"),
    url(r'^comment/(?P<cmt_id>[^/]+)/edit/$', views.reviewer_conference_equipment.EquipmentCommentEdit.as_view(), name="comment_edit"),
    ], 'equipment')

reviewer_conference_patterns = ([    
    url(r'^$', views.reviewer_conference.ConferenceDetail.as_view(), name="conference_detail"),
    url(r'^equipments/$', views.reviewer_conference.ConferenceEquipmentList.as_view(), name="equipment_list"),
    url(r'^equipment/(?P<eq_id>[^/]+)/', include(reviewer_conference_equipment_patterns)),    
    ], 'conference')

reviewer_document_patterns = ([    
    url(r'^online/$', views.reviewer_document.DocumentOnline.as_view(), name="document_online"),
    url(r'^download/$', views.reviewer_document.DocumentDownload.as_view(), name="document_download"),
    ], 'document')

reviewer_patterns = ([
    url(r'^detail/$', views.reviewer.ReviewerDetail.as_view(), name="reviewer_detail"),
    url(r'^edit/$', views.reviewer.ReviewerUpdate.as_view(), name="reviewer_edit"),
    url(r'^cpw/$', views.reviewer.ReviewerChangePassword.as_view(), name="reviewer_cpw"),

    url(r'^conferences/$', views.reviewer.ReviewerConferenceList.as_view(), name="conference_list"),
    url(r'^conference/(?P<conf_id>[^/]+)/', include(reviewer_conference_patterns)),    

    url(r'^document/(?P<doc_id>[^/]+)/', include(reviewer_document_patterns)),    
    ], 'reviewer')



# All
urlpatterns = [       
    url(r'^$', views.home.Welcome.as_view(), name='home'),
    url(r'^admin/', admin_site.urls, name="conference_admin"),
    url(r'^logout/', auth_views.logout, {'next_page': 'home'}, name='logout'),
        
    url(r'^designer/', include(designer_patterns)),
    url(r'^manager/', include(manager_patterns)),
    url(r'^reviewer/', include(reviewer_patterns)),
]
