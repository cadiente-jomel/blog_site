# Generated by Django 3.0.7 on 2020-11-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
