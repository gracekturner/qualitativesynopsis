from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('controlF/(?P<id>[\w\-]+)/$', views.controlF_view, name='controlF_view'),
    path('controlF/<id>/$', views.controlF_view, name = "controlF_view")

]
