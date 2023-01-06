from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            
        ]

        # This function is courtsey of https://stackoverflow.com/a/45623045/9666890
        # Django uses usernames by default. In this case we don't want the user to have to enter one, so we manipulate some data.
        # If the new to-be-saved user instance's username is not present, it will set the username to the to-be-saved user instance's email
        # Then, runs the function before save so there is a username when it is saved
        def set_username(sender, instance, **kwargs):
            if not instance.username:
                instance.username = f"{instance.first_name.capitalize()} {instance.last_name.capitalize()}"

        models.signals.pre_save.connect(set_username, sender=User)
