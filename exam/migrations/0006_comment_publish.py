# Generated by Django 5.0.8 on 2024-08-08 20:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]