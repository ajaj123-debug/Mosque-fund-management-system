# Generated by Django 5.1.1 on 2024-09-28 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_fund', '0004_alter_deduction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='category',
            field=models.CharField(choices=[('Imam Sahab Salary', 'इमाम साहब की सैलरी में'), ('Masjid ke Liye', 'मस्जिद में खर्च'), ('Normal Kharch', 'चालू खर्च')], max_length=30),
        ),
    ]
