# Generated by Django 2.1.1 on 2019-01-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190120_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.TextField(),
        ),
    ]