from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Poste(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blogd", kwargs={"pk": self.pk})

class PetOwner(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.lastName} {self.firstName}"

class Pet(models.Model):
    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pet = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.pet})"

class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.lastName} {self.firstName}"
      
class Appointment(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    service_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Appointment for {self.firstname} {self.lastname} - {self.time} {self.date}"

class Service(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    medication = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Service for {self.appointment}: {self.description}"
