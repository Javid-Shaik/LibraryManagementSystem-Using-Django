# Generated by Django 4.2.1 on 2023-07-29 10:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0025_registermodel_token_alter_borrowings_borrowed_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registermodel',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='borrowings',
            name='borrowed_date',
            field=models.DateField(default=datetime.date(2023, 7, 29)),
        ),
    ]
