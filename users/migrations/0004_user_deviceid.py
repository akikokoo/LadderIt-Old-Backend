# Generated by Django 4.2.6 on 2024-02-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_lastmissiondeletiondate"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="deviceId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
