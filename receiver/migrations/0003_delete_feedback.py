# Generated by Django 4.2.10 on 2024-03-12 19:08
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receiver', '0002_alter_order_date_time_feedback'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
