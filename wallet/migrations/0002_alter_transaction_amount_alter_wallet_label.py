# Generated by Django 5.1.7 on 2025-03-18 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=18),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='label',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
