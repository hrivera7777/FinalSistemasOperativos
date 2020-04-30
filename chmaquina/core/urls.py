from django.urls import path
from .views import HomePageView, HomePageView2

urlpatterns = [
    path('', HomePageView2.as_view(), name="home"),
]