# Generated by Django 3.0.7 on 2020-11-13 12:49

from django.db import migrations
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20201108_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=django_editorjs.fields.EditorJsField(),
        ),
    ]
