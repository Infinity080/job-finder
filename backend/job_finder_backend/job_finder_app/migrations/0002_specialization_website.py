# Generated by Django 5.1.2 on 2024-10-24 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_finder_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='website',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='specializations', to='job_finder_app.website'),
        ),
    ]
