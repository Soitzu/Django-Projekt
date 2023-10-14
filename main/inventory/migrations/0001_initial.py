# Generated by Django 4.2.5 on 2023-10-14 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('serialnumber', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statusname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('stnumber', models.IntegerField()),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.status'),
        ),
    ]
