# Generated by Django 4.2.6 on 2024-01-15 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missions", "0002_alter_mission_prevdate"),
    ]

    operations = [
        migrations.AddField(
            model_name="mission",
            name="category",
            field=models.CharField(default="null", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="mission",
            name="startDate",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="mission",
            name="title",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
