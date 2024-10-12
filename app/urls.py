from django.urls import path
from .views import HomePageView, AboutPageView, TaskPageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('activity/', AboutPageView.as_view(), name='activity'),
    path('task/', TaskPageView.as_view(), name='task'),
]
