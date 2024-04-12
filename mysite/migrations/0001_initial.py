# Generated by Django 4.0.4 on 2023-03-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('dept', models.CharField(blank=True, max_length=40, null=True)),
                ('credits', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('building', models.CharField(blank=True, max_length=20, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dept',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'instructor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('dept', models.CharField(blank=True, max_length=40, null=True)),
                ('total_credits', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Student',
                'managed': False,
            },
        ),
    ]
