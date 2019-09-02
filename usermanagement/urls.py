from django.conf.urls import url
from .views import *
from Crm.globals import get_queryset

app_name = 'usermanagement'

urlpatterns = [
    url(r'^TS7nEa2kl/$', login, name='login'),
    url(r'^$', login, name='login'),
    url(r'^TR6dWR9IOv/$',login_validate, name='login_validate'),
    url(r'^R9IOvTR6dW/$', dashboard, name='dashboard'),
    # url(r'^TR6dWOvR9I/$', mtodashboard, name='mtodashboard'),
    # url(r'^GST57bRoArTd/$', branchdashboard, name='branchdashboard'),
    url(r'^RoArTdGST57b/$', logout, name='logout'),
    url(r'^2CPfEMP1FR/$', User_list, name='User_list'),
    url(r'^2CPfEMP1FR/add/$', User_data_form, name='User_data_form'),
    url(r'^2CPfEMP1FR/edit/(?P<pk>[\w]+)$', user_data_edit, name='user_data_edit'),
    url(r'^2CPfEMP1FR/delete/(?P<pk>[\w]+)$', user_data_delete, name='user_data_delete'),
    url(r'^1FRfE435MP2CPf/$', User_profile, name='User_profile'),
    url(r'^1FRfEMP2CPf/$', Userrole_list, name='Userrole_list'),
    url(r'^1FRfEMP2CPf/add/$', Userrole_data_form, name='Userrole_data_form'),
    url(r'^1FRfEMP2CPf/edit/(?P<pk>[\w]+)$', userrole_data_edit, name='userrole_data_edit'),
    url(r'^1FRfEMP2CPf/delete/(?P<pk>[\w]+)$', userrole_data_delete, name='userrole_data_delete'),
    url(r'^6DTIAD68GTg/(?P<id>\w+)/(?P<user_role_type>[\w\-]+)/$', Privillage_list, name='Privillage_list'),
    url(r'^PrIv3Yll22gE/$', add_role_with_permission, name='add_role_with_permission'),
    url(r'^change_password/(?P<pk>[\w]+)$', change_password, name='change_password'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^forgetpassword/$', forget_password, name='forget_password'),
    url(r'^forget_email/$', forget_password_email, name='forget_password_email'),
    url(r'^2CPj67P1FR/$', moduleurl_list, name='moduleurl_list'),
    url(r'^2CP943FR/add/$', moduleurl_data_form, name='moduleurl_data_form'),
    url(r'^2CPf07jFR/edit/(?P<pk>[\w]+)$', moduleurl_data_edit, name='moduleurl_data_edit'),
    url(r'^2CPfE0mn3R/delete/(?P<pk>[\w]+)$', moduleurl_data_delete, name='moduleurl_data_delete'),
    url(r'^access_code/$', Access_code, name='Access_code'),
    url(r'^new_password/$', New_password, name='New_password'),
url(r'^get_queryset/(?P<app>[a-z, A-Z]+)/(?P<model>[a-z, A-Z, _]+)/$', get_queryset, name="get_queryset"),
]
