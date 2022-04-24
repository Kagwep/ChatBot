from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [

    path('', views.response),
    path('<str:pk>', views.ViewTurorial, name = "view-tutorial"),
    
    
]
