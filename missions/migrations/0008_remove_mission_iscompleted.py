# Generated by Django 4.2.6 on 2024-02-05 17:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("missions", "0007_alter_mission_prevdate_alter_mission_startdate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mission",
            name="isCompleted",
        ),
    ]
