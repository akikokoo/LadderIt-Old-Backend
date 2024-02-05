# Generated by Django 4.2.6 on 2024-02-04 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missions", "0006_alter_mission_prevdate_alter_mission_startdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="prevDate",
            field=models.DateTimeField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="mission",
            name="startDate",
            field=models.DateTimeField(max_length=50, null=True),
        ),
    ]
