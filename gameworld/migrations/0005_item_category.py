# Generated by Django 3.0.2 on 2020-01-23 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameworld', '0004_auto_20200123_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.IntegerField(default=0),
        ),
    ]
