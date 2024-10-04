# Generated by Django 5.1 on 2024-09-26 13:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_fund', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Tankhwah', 'Tankhwah'), ('Renovation', 'Renovation'), ('Khulla Saman', 'Khulla Saman')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
