# Generated by Django 4.2.16 on 2024-10-06 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community_fund', '0009_alter_deduction_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
