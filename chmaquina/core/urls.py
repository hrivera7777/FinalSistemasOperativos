from django.urls import path
from .views import HomePageView2, salirView

urlpatterns = [
    path('', HomePageView2.as_view(), name="home"),
    path('delete/', salirView.as_view(), name="salir"),
]