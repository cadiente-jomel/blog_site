# Generated by Django 3.0.7 on 2020-11-05 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201105_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.ImageField(blank=True, upload_to='uploads'),
        ),
    ]