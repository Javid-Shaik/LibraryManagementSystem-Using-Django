# Generated by Django 4.2.1 on 2023-07-29 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0026_registermodel_email_confirmed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]