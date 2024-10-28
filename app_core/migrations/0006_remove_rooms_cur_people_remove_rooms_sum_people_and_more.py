# Generated by Django 5.1.2 on 2024-10-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_core", "0005_alter_roomtransfer_room"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rooms",
            name="cur_people",
        ),
        migrations.RemoveField(
            model_name="rooms",
            name="sum_people",
        ),
        migrations.AddField(
            model_name="rooms",
            name="slot_available",
            field=models.IntegerField(default=10),
        ),
    ]
