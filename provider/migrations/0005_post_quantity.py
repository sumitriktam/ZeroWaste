# Generated by Django 4.2.10 on 2024-02-29 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0004_alter_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='quantity',
            field=models.CharField(default='1', max_length=25),
        ),
    ]
