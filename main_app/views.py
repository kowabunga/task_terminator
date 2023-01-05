from django.shortcuts import render
from .models import Task


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def home(request):
    return render(request, 'home.html')

class TaskList(LoginRequiredMixin, ListView):
    model = Task