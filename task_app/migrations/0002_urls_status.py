# Generated by Django 3.2.16 on 2022-10-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urls',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
