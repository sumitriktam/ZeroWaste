# Generated by Django 4.2.10 on 2024-02-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, upload_to='statics/provider/postpics'),
        ),
    ]