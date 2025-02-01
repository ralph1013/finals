from django.urls import path
from .views import HomePageView, AboutPageView, ServicePageView, AppointmentPageView, AppointmentRecordsView, AppointmentUpdateView, AppointmentDeleteView, BlogListView, BlogUpdateView, BlogDeleteView, appointment_submit, get_appointments, get_appointments_for_day, signup, login_view, logout_view

urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('service/', ServicePageView.as_view(), name='service'),
    path('appointment/', AppointmentPageView.as_view(), name='appointment'),
    path('appointment/records/', AppointmentRecordsView.as_view(), name='appointment_records'),
    path('appointments/edit/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('appointments/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('submit-appointment/', appointment_submit, name='appointment_submit'),
    path('get-appointments/', get_appointments, name='get_appointments'),
    path('appointments/', get_appointments_for_day, name='get_appointments_for_day'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
