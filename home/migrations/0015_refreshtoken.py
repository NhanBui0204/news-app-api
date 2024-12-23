# Generated by Django 5.1.3 on 2024-11-27 07:16

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_user_options_user_address_user_created_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='refresh_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'refreshtoken',
            },
        ),
    ]
