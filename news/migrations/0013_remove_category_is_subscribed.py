# Generated by Django 4.2.6 on 2023-10-29 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_category_is_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_subscribed',
        ),
    ]
