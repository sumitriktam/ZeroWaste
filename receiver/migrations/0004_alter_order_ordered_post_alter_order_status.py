# Generated by Django 4.2.10 on 2024-03-27 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0016_scorehistory'),
        ('receiver', '0003_delete_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='provider.post'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('accept', 'Accept'), ('reject', 'Reject'), ('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=10),
        ),
    ]