# Generated by Django 3.0.7 on 2020-08-03 12:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenPro',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('parcela', models.CharField(max_length=254)),
                ('urlSentinel', models.CharField(max_length=254)),
                ('imagen', models.CharField(max_length=254)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
