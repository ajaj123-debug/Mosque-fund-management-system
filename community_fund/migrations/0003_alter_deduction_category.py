# Generated by Django 5.1.1 on 2024-09-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_fund', '0002_deduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='category',
            field=models.CharField(choices=[('Imam Sahab Salary', 'Imam Sahab Salary'), ('Masjid ke Liye', 'Masjid ke Liye'), ('Normal Kharch', 'Normal Kharch'), ('Milad', 'Milad')], max_length=20),
        ),
    ]
