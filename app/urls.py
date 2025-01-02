from django.urls import path
from .views import HomePageView, AboutPageView, ServicePageView, AppointmentPageView, BlogListView, BlogDetailView, appointment_submit, get_appointments

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('service/', ServicePageView.as_view(), name='service'),
    path('appointment/', AppointmentPageView.as_view(), name='appointment'),
    path('submit-appointment/', appointment_submit, name='appointment_submit'),
    path('get-appointments/', get_appointments, name='get_appointments'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail')
]
