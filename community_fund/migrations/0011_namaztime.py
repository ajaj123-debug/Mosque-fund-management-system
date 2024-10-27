# Generated by Django 4.2.10 on 2024-10-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_fund', '0010_remove_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='NamazTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fajr_time', models.TimeField()),
                ('dhuhr_time', models.TimeField()),
                ('asr_time', models.TimeField()),
                ('maghrib_time', models.TimeField()),
                ('isha_time', models.TimeField()),
            ],
        ),
    ]