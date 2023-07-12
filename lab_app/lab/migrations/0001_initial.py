# Generated by Django 4.2.3 on 2023-07-12 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('description', models.TextField(max_length=800)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Samples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=800)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('experiment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.experiments')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, unique=True)),
                ('email', models.CharField(max_length=85, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('sample_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.samples')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.tests')),
            ],
        ),
        migrations.CreateModel(
            name='Invitations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_from', models.IntegerField()),
                ('group_id', models.IntegerField(null=True)),
                ('token', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.users')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('lider_id', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('users_id', models.ManyToManyField(null=True, to='lab.users')),
            ],
        ),
        migrations.AddField(
            model_name='experiments',
            name='group_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lab.groups'),
        ),
    ]
