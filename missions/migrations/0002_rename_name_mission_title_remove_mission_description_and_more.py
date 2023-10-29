# Generated by Django 4.2.6 on 2023-10-29 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("missions", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mission",
            old_name="name",
            new_name="title",
        ),
        migrations.RemoveField(
            model_name="mission",
            name="description",
        ),
        migrations.AddField(
            model_name="mission",
            name="timeZone",
            field=models.CharField(default="0", max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="mission",
            name="numberOfDays",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="mission",
            name="prevDate",
            field=models.DateTimeField(),
        ),
    ]
