
from django.contrib import admin
from django.urls import path

from health_app import views

urlpatterns = [
    path('',views.firstpage,name="firstpage"),
    # path('',views.login,name="login"),
    path('login',views.login,name="login"),
    path('changepsswd',views.changepsswd,name="changepsswd"),
    path('vchangepsswd',views.vchangepsswd,name="vchangepsswd"),
    path('home',views.home,name="home"),
    path('home2',views.home2,name="home2"),
    path('assignworkcode',views.assignworkcode,name="assignworkcode"),
    path('assign_works',views.assign_works,name="assign_works"),
    path('check_uname_web',views.check_uname_web,name="check_uname_web"),
    path('add_works',views.add_works,name="add_works"),
    path('edit_works/<int:id>',views.edit_works,name="edit_works"),
    path('editwork',views.editwork,name="editwork"),
    path('chatwith_cartkr',views.chatwith_cartkr,name="chatwith_cartkr"),
    path('manag_caminfo',views.manag_caminfo,name="manag_caminfo"),
    path('manage_caretkr',views.manage_caretkr,name="manage_caretkr"),
    path('add_caretkr',views.add_caretkr,name="add_caretkr"),
    path('addcartkr',views.addcartkr,name="addcartkr"),
    path('deletepatientinfo/<int:id>',views.deletepatientinfo,name="deletepatientinfo"),
    path('addpatientinfo',views.addpatientinfo,name="addpatientinfo"),
    path('edit_caretkr/<int:id>',views.edit_caretkr,name="edit_caretkr"),
    path('edit_caretkr1',views.edit_caretkr1,name="edit_caretkr1"),
    path('edit_crtkr',views.edit_crtkr,name="edit_crtkr"),
    path('search_crtkr',views.search_crtkr,name="search_crtkr"),
    path('manage_patient_info',views.manage_patient_info,name="manage_patient_info"),
    path('add_patient_info',views.add_patient_info,name="add_patient_info"),
    path('edit_patient_info/<int:id>',views.edit_patient_info,name="edit_patient_info"),
    path('medicin_notifctn',views.medicin_notifctn,name="medicin_notifctn"),
    path('edit_patient_info1',views.edit_patient_info1,name="edit_patient_info1"),
    path('editpatientinfo_post',views.editpatientinfo_post,name="editpatientinfo_post"),
    path('patient_needs',views.patient_needs,name="patient_needs"),
    path('sendreplycode',views.sendreplycode,name="sendreplycode"),
    path('complaint_search',views.complaint_search,name="complaint_search"),
    path('view_complnt',views.view_complnt,name="view_complnt"),
    path('send_rply/<int:id>',views.send_rply,name="send_rply"),
    path('view_patient_recods/<int:id>',views.view_patient_recods,name="view_patient_recods"),
    path('logincode',views.logincode,name="logincode"),
    path('dlt_ckr/<int:id>',views.dlt_ckr,name='dlt_ckr'),
    path('deleteassign/<int:id>',views.deleteassign,name='deleteassign'),
    path('edit_workscodesss',views.edit_workscodesss,name='edit_workscodesss'),
    path('manage_patient_info_search',views.manage_patient_info_search,name='manage_patient_info_search'),
    path('view_patient',views.view_patient,name='view_patient'),
    path('p_h_reports',views.p_h_reports,name='p_h_reports'),
    path('viewprecords1',views.viewprecords1,name='viewprecords1'),
    path('assn_work_search',views.assn_work_search,name='assn_work_search'),
    path('medcn_notfcn_verify/<int:id>',views.medcn_notfcn_verify,name='medcn_notfcn_verify'),
    path('activecaretkr/<int:id>',views.activecaretkr,name='activecaretkr'),
    path('inactivecaretkr/<int:id>',views.inactivecaretkr,name='inactivecaretkr'),
    path('patient_needs_verify/<int:id>',views.patient_needs_verify,name='patient_needs_verify'),
    path('medcn_notfcn_search',views.medcn_notfcn_search,name='medcn_notfcn_search'),
    path('patient_needs_search',views.patient_needs_search,name='patient_needs_search'),
    path('add_cam',views.add_cam,name='add_cam'),
    path('addcam_info',views.addcam_info,name='addcam_info'),
    path('editcam/<int:id>',views.editcam,name='editcam'),
    path('editcam_info',views.editcam_info,name='editcam_info'),
    path('deletecam_info/<int:id>',views.deletecam_info,name='deletecam_info'),
    path('fall_detecion',views.fall_detecion,name='fall_detecion'),
    path('logout',views.logout,name='logout'),
    path('getAlert',views.getAlert,name='getAlert'),
    path('view_alert',views.view_alert,name='view_alert'),
    # path('update_alert',views.update_alert,name='update_alert'),
    path('update_alertall',views.update_alertall,name='update_alertall'),
    path('manage_patient_info_update_death/<id>',views.manage_patient_info_update_death,name='manage_patient_info_update_death'),



path('chatwithuser', views.chatwithuser, name='chatwithuser'),
path('chatview', views.chatview, name='chatview'),
path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),













    # ----------------------android--------------------
    path('logincodeand',views.logincodeand,name='logincodeand'),
    path('viewassginedwork',views.viewassginedwork,name='viewassginedwork'),
    path('check_email_web',views.check_email_web,name='check_email_web'),
    path('check_phone_web',views.check_phone_web,name='check_phone_web'),
    path('updatework',views.updatework,name='updatework'),
    path('change_password',views.change_password,name='change_password'),
    path('viewpatient_info',views.viewpatient_info,name='viewpatient_info'),
    path('update_patient_info',views.update_patient_info,name='update_patient_info'),
    path('viewmang_pills_setalaram',views.viewmang_pills_setalaram,name='viewmang_pills_setalaram'),
    path('addreminder',views.addreminder,name='addreminder'),
    path('mednoti',views.mednoti,name='mednoti'),
    path('view_medicine_info',views.view_medicine_info,name='view_medicine_info'),
    path('delete_medicine_info',views.delete_medicine_info,name='delete_medicine_info'),
    path('view_suffict_medicine',views.view_suffict_medicine,name='view_suffict_medicine'),
    path('add_s_med_info',views.add_s_med_info,name='add_s_med_info'),
    path('add_medicine',views.add_medicine,name='add_medicine'),
    path('delete_s_med_info',views.delete_s_med_info,name='delete_s_med_info'),
    path('search_s_med_info',views.search_s_med_info,name='search_s_med_info'),
    path('view_patient_needs',views.view_patient_needs,name='view_patient_needs'),
    path('add_p_needs',views.add_p_needs,name='add_p_needs'),
    path('delete_p_needs',views.delete_p_needs,name='delete_p_needs'),
    path('search_p_needs',views.search_p_needs,name='search_p_needs'),
    path('view_med',views.view_med,name='view_med'),
    path('c_send_complaint',views.c_send_complaint,name='c_send_complaint'),
    path('view_complaint',views.view_complaint,name='view_complaint'),
    path('delete_complaint',views.delete_complaint,name='delete_complaint'),
    path('in_message2',views.in_message2,name='in_message2'),
    path('view_message2',views.view_message2,name='view_message2'),
    path('chatwithuser',views.chatwithuser,name='chatwithuser'),



]
