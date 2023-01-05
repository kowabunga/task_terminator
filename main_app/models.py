from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField()
    date_added = models.DateTimeField()
    due_date = models.DateTimeField()
    priority = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)]
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'_id': self.id})

    class Meta:
        ordering = ['-due_date']

