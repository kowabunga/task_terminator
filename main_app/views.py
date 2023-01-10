from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.mail import send_mail

from .forms import SignUpForm, UpdateUserForm

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


@login_required
def user_profile_page(request):

    tasks = Task.objects.filter(user=request.user)

    return render(request, "user/index.html", {"user": request.user, "tasks": tasks})


class UpdatePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = "/password_edit_success"
    template_name = "main_app/change_password.html"


# This acts as a "redirect" url for the password change success url
# This "inbetween" route allows us to send the email confirming to the user that their password has been changed
def password_edit_success(request):
    # subject, message, to_email
    send_email(
        "Password Updated",
        "Thank you for using Task Terminator. Your password has been successfully updated.",
        request.user.email,
    )
    return redirect("user_profile")


@login_required
def update_user(request):
    error_message = ""
    user = request.user
    if request.method == "POST":
        # check if form is valid
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            # if form is valid, replace value of "user.x" with form submitted "request.POST.x" and save the user, thereby updating it
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()

            send_email(
                "User Updated",
                "Thank you for using Task Terminator. The information you requested be updated has been updated.",
                user.email,
            )

            return redirect("user_profile")
        else:
            error_message = "Invalid update - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UpdateUserForm(initial={"first_name": user.first_name, "last_name": user.last_name, "email": user.email})
    context = {"form": form, "error_message": error_message}

    return render(request, "user/update.html", context)
