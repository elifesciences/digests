# Generated by Django 2.0.7 on 2018-07-25 08:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Digest',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField()),
                ('image', django.contrib.postgres.fields.jsonb.JSONField()),
                ('impactStatement', models.TextField(blank=True, null=True)),
                ('published', models.DateTimeField()),
                ('relatedContent', django.contrib.postgres.fields.jsonb.JSONField()),
                ('subjects', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('title', models.CharField(max_length=255)),
                ('updated', models.DateTimeField(null=True)),
            ],
        ),
    ]
