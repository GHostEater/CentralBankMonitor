from django.conf.urls import url
from django.contrib.auth.views import login, logout
from bankMonitor import views

urlpatterns = [
    url(r'^$', login, {'template_name': 'login.html', 'redirect_authenticated_user': True}),
    url(r'^logout/$', logout, name='logout'),

    url(r'^home/$', views.home, name='home'),

    url(r'^banks/$', views.BankView.as_view(), name='banks'),
    url(r'^banks/add/$', views.BankCreate.as_view(), name='bank-add'),
    url(r'^banks/edit/(?P<pk>[0-9]+)/$', views.BankUpdate.as_view(), name='bank-edit'),
    url(r'^banks/delete/(?P<pk>[0-9]+)/$', views.BankDelete.as_view(), name='bank-delete'),

    url(r'^bank-officers/$', views.bank_officer, name='bank-officers'),
    url(r'^bank-officers/add/$', views.bank_officer_create, name='bank-officer-add'),
    url(r'^bank-officers/edit/(?P<id>[0-9]+)/$', views.bank_officer_edit, name='bank-officer-edit'),
    url(r'^bank-officers/delete/(?P<pk>[0-9]+)/$', views.BankOfficerDelete.as_view(), name='bank-officer-delete'),

    url(r'^transactions/$', views.trans, name='trans'),
    url(r'^transactions/add/$', views.trans_add, name='trans-add'),

    url(r'^special-transactions/$', views.spec_trans, name='spec-trans'),
    url(r'^special-transactions/request/$', views.spec_trans_request, name='spec-trans-request'),
    url(r'^special-transactions/process/(?P<id>[0-9]+)/$', views.spec_trans_process, name='spec-trans-process'),

    url(r'^monitor/$', views.monitor, name='monitor'),
    url(r'^transaction-reports/$', views.trans_report, name='trans-report'),
    url(r'^special-transaction-reports/$', views.spec_trans_report, name='spec-trans-report'),
]
