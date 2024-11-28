# Generated by Django 5.1.3 on 2024-11-28 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=3),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=3),
        ),
    ]
