# Generated by Django 5.0.1 on 2024-01-08 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_entry_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='owner',
        ),
    ]
