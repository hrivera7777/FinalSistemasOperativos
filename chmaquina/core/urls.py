from django.urls import path
from .views import HomePageView2, salirView, InicioPageView

urlpatterns = [
    path('', InicioPageView.as_view(), name="home"),
    path('fcfs/', HomePageView2.as_view(), name="fcfs"),
    path('delete/', salirView.as_view(), name="salir"),
    
]