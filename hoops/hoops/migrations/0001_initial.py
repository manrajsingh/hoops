# Generated by Django 4.0.3 on 2022-03-22 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoops.league')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoops.player')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_on', models.DateTimeField(auto_now_add=True)),
                ('host_score', models.IntegerField()),
                ('guest_score', models.IntegerField()),
                ('guest', models.ManyToManyField(related_name='guest', to='hoops.player')),
                ('host', models.ManyToManyField(related_name='host', to='hoops.player')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoops.league')),
            ],
        ),
    ]