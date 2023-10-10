# Generated by Django 4.2.5 on 2023-10-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_todo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='time',
        ),
        migrations.AddField(
            model_name='todo',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='hour',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='minute',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='second',
            field=models.IntegerField(null=True),
        ),
    ]
