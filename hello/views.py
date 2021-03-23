from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import requests
<<<<<<< HEAD
import os
=======
>>>>>>> aee451704a9c7df749d0aa638f764f64c3aabe67

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
