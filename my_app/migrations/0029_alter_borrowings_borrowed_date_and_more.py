# Generated by Django 4.2.1 on 2023-07-31 15:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0028_alter_borrowings_borrowed_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowings',
            name='borrowed_date',
            field=models.TimeField(default=datetime.date(2023, 7, 31)),
        ),
        migrations.AlterField(
            model_name='borrowings',
            name='due_date',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='borrowings',
            name='return_date',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
