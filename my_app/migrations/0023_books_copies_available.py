# Generated by Django 4.2.1 on 2023-06-27 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0022_rename_borrowing_date_borrowings_borrowed_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='copies_available',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]