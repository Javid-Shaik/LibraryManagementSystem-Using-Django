# Generated by Django 4.2.1 on 2023-06-01 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0019_alter_books_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowings',
            name='fine_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]