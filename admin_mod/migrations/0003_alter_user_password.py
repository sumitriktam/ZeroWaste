# Generated by Django 4.2.10 on 2024-02-29 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mod', '0002_admin_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64),
        ),
    ]