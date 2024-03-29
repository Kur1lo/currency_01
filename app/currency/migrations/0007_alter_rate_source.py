# Generated by Django 4.0.6 on 2022-08-28 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0006_rate_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='rates',
                                    to='currency.source'
                                    ),
        ),
    ]
