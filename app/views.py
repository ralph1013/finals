from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from .models import Poste, Appointment
import calendar
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'app/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('dashboard')            

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
    return redirect(f'/appointment/?month={date.split("-")[1]}&day={date.split("-")[0]}&year={date.split("-")[0]}')

def get_appointments(request):
   
    appointments = AppointmentPageView.objects.all()
    
    events = []
    for appointment in appointments:
        events.append({
        'title': f"{appointment.first_name} {appointment.last_name} - {appointment.service_type}",
        'start': f"{appointment.date}T{appointment.time}",
    })
    return JsonResponse(events, safe=False)   

def get_appointments_for_day(request):
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    appointments = Appointment.objects.filter(date__day=day, date__month=month, date__year=year)
    appointment_data = [{
        'id': appt.id,
        'name': f"{appt.firstname} {appt.lastname}",
        'service': appt.service_type,
        'time': appt.time.strftime("%H:%M"),
    } for appt in appointments]
    
    return JsonResponse(appointment_data, safe=False)

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
        booking_status = {day: {"status": "not_booked", "appointments": []} for day in range(1, 32)}
        for appt in appointments:
            day = appt.date.day
            booking_status[day]["appointments"].append(appt)
            if len(booking_status[day]["appointments"]) >= 5:  
                booking_status[day]["status"] = "fully_booked"
            else:
                booking_status[day]["status"] = "available"
                
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
            'appointments': appointments, 
        })
        return context
    
    def appoinment(request):
        return render(request, 'appointment.html')

class BlogListView(CreateView, ListView):
    model = Poste
    template_name = 'app/blog.html'
    fields = ['body', 'image']
    success_url = reverse_lazy('blog_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Poste.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            body = request.POST.get('body')
            if body and request.user.is_authenticated:
                post = Poste(user=request.user, body=body)
                post.save()
            return redirect('blog_list')

class AppointmentRecordsView(TemplateView):
    template_name = 'app/record.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.all()
        return context

class AppointmentUpdateView(UpdateView):
    model = Appointment
    template_name = 'app/edit_appointment.html'
    fields = ['firstname', 'lastname', 'contact', 'email', 'date', 'time', 'service_type']
    success_url = reverse_lazy('appointment_records')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.object
        return context

class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'app/delete_appoinment.html'
    success_url = reverse_lazy('appointment_records')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.get_object()
        return context

class BlogUpdateView(UpdateView):
    model = Poste
    template_name = 'app/blog_edit.html'
    fields = ['body', 'image']
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class BlogDeleteView(DeleteView):
    model = Poste
    template_name = 'app/blog_delete.html'
    success_url = reverse_lazy('blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context