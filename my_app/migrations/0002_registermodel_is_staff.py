# Generated by Django 4.2.1 on 2023-05-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registermodel',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]