# Generated by Django 3.0.2 on 2020-01-21 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0002_auto_20200121_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='rm_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
