from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from .models import Poste, Appointment
import calendar
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import PostForm

def appointment_submit(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        service_type = request.POST.get('service_type')

        Appointment.objects.create(
        firstname = firstname,
        lastname = lastname,
        contact = contact,
        email = email,
        date = date,
        time = time,
        service_type = service_type
    )
    messages.success(request, 'Appointment booked successfully!')
    return redirect(f'/appointment/?month={date.split("-")[1]}&year={date.split("-")[0]}')

def get_appointments(request):
   
    appointments = AppointmentPageView.objects.all()
    
    events = []
    for appointment in appointments:
        events.append({
        'title': f"{appointment.first_name} {appointment.last_name} - {appointment.service_type}",
        'start': f"{appointment.date}T{appointment.time}",
    })
    return JsonResponse(events, safe=False)   

class HomePageView(TemplateView):
    template_name = 'app/dashboard.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'
    
class ServicePageView(TemplateView):
    template_name = 'app/service.html'

class AppointmentPageView(TemplateView):
    template_name = 'app/appointment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year', datetime.now().year)
        month = self.request.GET.get('month', datetime.now().month)
        year = int(year)
        month = int(month)
        
        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(year, month)
        month_name = calendar.month_name[month]
        today = datetime.now().day
        
        if month == 1:
            previous_month = 12
            previous_year = year - 1
        else:
            previous_month = month - 1
            previous_year = year
        
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        years = range(year - 5, year + 6)
        
        appointments = Appointment.objects.filter(date__year=year, date__month=month)
        booking_status = {day: "not_booked" for day in range(1, 32)}
        for appt in appointments:
            day = appt.date.day
            daily_appointments = appointments.filter(date__day=day)
            if daily_appointments.count() >= 5:  # Assume 5 is the max slots per day
                booking_status[day] = "fully_booked"
            else:
                booking_status[day] = "available"
        
        context.update({
            'year': int(year),
            'month': int(month),
            'month_name': month_name,
            'month_days': month_days,
            'years': years,
            'today': today,
            'previous_month': previous_month,
            'previous_year': previous_year,
            'next_month': next_month,
            'next_year': next_year,
            'booking_status': booking_status,
        })
        return context
    
    def appoinment(request):
        return render(request, 'appointment.html')

class BlogListView(TemplateView):
    template_name = 'app/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Poste.objects.all()
        context['form'] = PostForm()  # Include the form for creating a new post
        return context

    def post(self, request):
        # Handle creating a new post
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return JsonResponse({'status': 'success', 'post': {'id': post.id, 'title': post.title, 'body': post.body}})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

class BlogDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Poste, pk=pk)
        return JsonResponse({'post': {'id': post.id, 'title': post.title, 'body': post.body}})

    def post(self, request, pk):
        if 'delete' in request.POST:
            post = get_object_or_404(Poste, pk=pk)
            post.delete()
            return JsonResponse({'status': 'success'})
        else:
            post = get_object_or_404(Poste, pk=pk)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                return JsonResponse({'status': 'success', 'post': {'id': post.id, 'title': post.title, 'body': post.body}})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})

    def delete(self, request, pk):
        post = get_object_or_404(Poste, pk=pk)
        post.delete()
        return JsonResponse({'status': 'success'})