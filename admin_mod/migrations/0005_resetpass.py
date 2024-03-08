# Generated by Django 4.2.10 on 2024-03-04 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_mod', '0004_user_zerowaste_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resetpass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forget_password_token', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admin_mod.user')),
            ],
        ),
    ]
