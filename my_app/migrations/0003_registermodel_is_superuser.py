# Generated by Django 4.2.1 on 2023-05-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_registermodel_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='registermodel',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]