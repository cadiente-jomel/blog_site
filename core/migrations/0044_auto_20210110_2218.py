# Generated by Django 3.1.5 on 2021-01-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20210110_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile',
            field=models.ImageField(default='/profile/default.jpg', upload_to='profile', verbose_name='Profile_image'),
        ),
    ]
