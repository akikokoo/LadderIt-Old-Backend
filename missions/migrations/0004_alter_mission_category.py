# Generated by Django 4.2.6 on 2024-01-15 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missions", "0003_mission_category_mission_startdate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="category",
            field=models.CharField(max_length=25, null=True),
        ),
    ]
