# Generated by Django 3.0.7 on 2021-06-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newimgprocess', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newimagenpro',
            name='id_parcelas',
            field=models.CharField(max_length=254, null=True),
        ),
    ]