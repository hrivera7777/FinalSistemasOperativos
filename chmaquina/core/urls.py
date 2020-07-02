from django.urls import path
from .views import HomePageView2, salirView, InicioPageView,SPNView, PrioridadNoExpView, SRTNView, RRView

urlpatterns = [
    path('', InicioPageView.as_view(), name="home"),
    path('fcfs/', HomePageView2.as_view(), name="fcfs"),
    path('spn/', SPNView.as_view(), name="spn"),
    path('srtn/', SRTNView.as_view(), name="srtn"),
    path('prioridadNoExp/', PrioridadNoExpView.as_view(), name="prioridadNoExp"),
    path('rr/', RRView.as_view(), name="rr"),
    path('delete/', salirView.as_view(), name="salir"),
    
]