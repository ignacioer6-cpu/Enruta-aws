from django.urls import path
from . import views

urlpatterns = [
    path('',views.inicio),
    path('registroC/',views.registroC),
    path('registroP/',views.registroP),
    path('procesar/',views.procesar),
    path('panel/', views.panel_admin),
]