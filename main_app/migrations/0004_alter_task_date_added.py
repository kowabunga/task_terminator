# Generated by Django 4.1.4 on 2023-01-11 21:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0003_alter_task_options_alter_task_date_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="date_added",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 1, 11, 16, 59, 5, 347384)
            ),
        ),
    ]