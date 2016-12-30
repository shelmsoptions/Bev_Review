from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_form', views.add_form, name='add_form'),
    url(r'^add', views.add, name='add'),
    url(r'^edit/(?P<id>\d+)', views.edit, name='edit'),
    url(r'^distiller_info/(?P<id>\d+)', views.distiller_info, name='distiller_info'),
    url(r'^edit_distiller/(?P<id>\d+)', views.edit_distiller, name='edit_distiller'),
    url(r'^update_distiller/(?P<id>\d+)', views.update_distiller, name='update_distiller'),
    url(r'^delete/(?P<id>\d+)', views.delete, name='delete'),
    url(r'^delete_distiller/(?P<id>\d+)', views.delete_distiller, name='delete_distiller'),


]