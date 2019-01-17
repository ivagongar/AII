# Generated by Django 2.1.4 on 2019-01-04 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('type', models.TextField()),
                ('rating', models.IntegerField()),
                ('cost', models.FloatField()),
                ('on_sale_cost', models.FloatField()),
                ('plus_cost', models.FloatField()),
                ('start_date_on_sale', models.DateTimeField()),
                ('end_date_on_sale', models.DateTimeField()),
                ('release_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('games', models.ManyToManyField(related_name='libraries', to='app.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.ManyToManyField(related_name='games', to='app.Genre'),
        ),
        migrations.AddField(
            model_name='game',
            name='offer_categories',
            field=models.ManyToManyField(related_name='games', to='app.OfferCategory'),
        ),
    ]
