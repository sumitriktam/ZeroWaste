# Generated by Django 4.2.10 on 2024-03-15 11:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mod', '0008_emailverification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='admin',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin',
            name='location',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20),
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=64),
        ),
    ]