# Generated by Django 5.1.3 on 2024-11-25 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_content_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='image',
            new_name='image_url',
        ),
        migrations.AddField(
            model_name='content',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='contents/%Y/%m'),
        ),
    ]