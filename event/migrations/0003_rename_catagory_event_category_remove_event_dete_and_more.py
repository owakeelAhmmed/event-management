# Generated by Django 5.2.3 on 2025-07-04 08:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_category_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='catagory',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='event',
            name='dete',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.date(2025, 7, 4)),
            preserve_default=False,
        ),
    ]
