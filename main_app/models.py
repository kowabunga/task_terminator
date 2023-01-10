from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from twilio.rest import Client
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.now())
    due_date = models.DateTimeField()
    priority = models.IntegerField(default=1, validators=[MaxValueValidator(3), MinValueValidator(1)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["-due_date"]

    def save(self, *args, **kwargs):

        account_sid = env("TWILIO_ACCOUNT_SID")
        auth_token = env("TWILIO_AUTH_TOKEN")
        print(env("TWILIO_ACCOUNT_SID"))
        print(env("TWILIO_AUTH_TOKEN"))
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"{ self.title } is due at { self.due_date }. This task is priority level: { self.priority } Here is your task description: { self.description }",
            from_="+13393304638",
            status_callback="http://postb.in/1234abcd",
            to="+17204721204",
        )

        print(message.sid)
        return super().save(*args, **kwargs)
