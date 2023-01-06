from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.mail import send_mail

from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

from .models import Task


def send_email(subject, message, to_email, from_email="taskterminator@outlook.com"):
    send_mail(subject, message, from_email, [to_email], fail_silently=False)


# Create your views here.
def home(request):
    return render(request, "home.html")


def sign_up(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = SignUpForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            print(user)
            # user.username = user.first_name
            # This is how we log a user in via code
            send_email(
                "Welcome to Task Terminator!",
                "Thank you for signing up to task terminator. Take a look around the site to see what it can do for you.",
                # replace this with user.email
                user.email,
            )
            login(request, user)
            return redirect("tasks_index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = SignUpForm()
    context = {"form": form, "error_message": error_message}

    return render(request, "registration/signup.html", context)


class TaskList(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        # Get the queryset from the Task class and filter the results, selecting only the tasks belonging to the logged in user
        return super().get_queryset().filter(user=self.request.user)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = [
        "title",
        "description",
        "completed",
        "due_date",
        "priority",
    ]


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = "/tasks/"
