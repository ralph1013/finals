from django.shortcuts import render
from django.views.generic import TemplateView
import calendar
from calendar import HTMLCalendar

class HomePageView(TemplateView):
    template_name = 'app/dashboard.html'

class AboutPageView(TemplateView):
    template_name = 'app/activity.html'
    
class TaskPageView(TemplateView):
    template_name = 'app/task.html'
    
   