# Generated by Django 4.2.10 on 2024-02-29 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0008_toysdes_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='toysdes',
            old_name='status',
            new_name='condition',
        ),
    ]
