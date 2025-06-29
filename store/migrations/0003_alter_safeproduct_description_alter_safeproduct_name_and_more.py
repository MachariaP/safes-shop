# Generated by Django 5.2.1 on 2025-06-09 07:36

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_safeproduct_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safeproduct',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='safeproduct',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='safeproduct',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
