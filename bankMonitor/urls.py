from django.conf.urls import url
from django.contrib.auth.views import login, logout
from bankMonitor import views

urlpatterns = [
    url(r'^$', login, {'template_name': 'login.html'}),
    url(r'^logout/', logout, name='logout'),

    url(r'^home/$', views.home, name='home'),

    url(r'^banks/$', views.BankView.as_view(), name='banks'),
    url(r'^banks/add/$', views.BankCreate.as_view(), name='bank-add'),
    url(r'^banks/edit/(?P<pk>[0-9]+)/$', views.BankUpdate.as_view(), name='bank-edit'),
    url(r'^banks/delete/(?P<pk>[0-9]+)/$', views.BankDelete.as_view(), name='bank-delete'),

    url(r'^officers/$', views.OfficerView.as_view(), name='officers'),
    url(r'^officers/add/$', views.OfficerCreate.as_view(), name='officer-add'),
    url(r'^officers/edit/(?P<pk>[0-9]+)/$', views.OfficerUpdate.as_view(), name='officer-edit'),
    url(r'^officers/delete/(?P<pk>[0-9]+)/$', views.OfficerDelete.as_view(), name='officer-delete'),

    url(r'^transactions/$', views.trans, name='trans'),
    url(r'^transactions/add/', views.trans_add, name='trans-add'),

    url(r'^monitor/', views.monitor, name='monitor'),
]
