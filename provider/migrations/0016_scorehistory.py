# Generated by Django 4.2.10 on 2024-03-17 20:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mod', '0010_adminreg'),
        ('provider', '0015_post_latlong'),
    ]

    operations = [
        migrations.CreateModel(
            name='scoreHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('score', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_mod.user')),
            ],
        ),
    ]