# Generated by Django 4.2.1 on 2023-05-27 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_registermodel_groups_registermodel_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='registermodel',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]