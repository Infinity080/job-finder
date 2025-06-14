# Generated by Django 5.2.1 on 2025-05-29 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_finder_app', '0002_specialization_website'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialization',
            name='amount',
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_text', models.TextField()),
                ('job_roles', models.JSONField(blank=True, null=True)),
                ('education', models.JSONField(blank=True, null=True)),
                ('skills', models.JSONField(blank=True, null=True)),
                ('experience_level', models.CharField(blank=True, max_length=64, null=True)),
                ('employment_type', models.JSONField(blank=True, null=True)),
                ('date_scraped', models.DateField(auto_now_add=True)),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_finder_app.specialization')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_finder_app.website')),
            ],
        ),
    ]
