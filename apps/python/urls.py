from django.conf.urls import url
from . import views         
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),    
    url(r'^login', views.validate),
    url(r'^success', views.success),
    url(r'^travels', views.travels),
    url(r'^addtrip', views.addtrip),
    url(r'^add_a_trip', views.add_a_trip),
    url(r'^logout', views.logout),
    url(r'^view/(?P<id>\d+)$', views.this_trip),
    url(r'^join/(?P<id>\d+)$', views.join_trip),
    url(r'^cancel/(?P<id>\d+)$', views.cancel_trip),
    url(r'^delete/(?P<id>\d+)$', views.delete_trip),


]                           
