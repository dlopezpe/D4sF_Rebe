# Generated by Django 3.0.7 on 2023-12-13 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trazas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trazas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_user', models.TextField(blank=True, max_length=255, null=True)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('updated_model', models.TextField(blank=True, max_length=255, null=True)),
                ('crud', models.TextField(blank=True, max_length=1000, null=True)),
                ('ip_user', models.GenericIPAddressField(blank=True, null=True)),
                ('enterprise_code', models.TextField(blank=True, max_length=255, null=True)),
                ('user_email', models.EmailField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'trazas',
            },
        ),
    ]
