from django.urls import path
from .views import HomePageView2, salirView, InicioPageView,SPNView, PrioridadNoExpView

urlpatterns = [
    path('', InicioPageView.as_view(), name="home"),
    path('fcfs/', HomePageView2.as_view(), name="fcfs"),
    path('spn/', SPNView.as_view(), name="spn"),
    path('prioridadNoExp/', PrioridadNoExpView.as_view(), name="prioridadNoExp"),
    path('delete/', salirView.as_view(), name="salir"),
    
]