# Generated by Django 5.1.3 on 2024-12-02 01:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_content_image_file_alter_category_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
