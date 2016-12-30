from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^login$', views.login, name='login'),
    # # Dont' FORGET THE COMMAS!!!!! # #
    url(r'^register_login$', views.register_login, name='log_reg'),
    url(r'^home$', views.home, name='home'),
    url(r'^home/(?P<id>\d+)/delete$', views.delete, name='delete'),
    url(r'^home/(?P<id>\d+)/edit', views.edit, name='edit'),
    url(r'^home/(?P<id>\d+)/update_user', views.update_user, name='update_user'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
]