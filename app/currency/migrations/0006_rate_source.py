# Generated by Django 4.0.6 on 2022-08-28 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0005_remove_rate_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='source',
            field=models.ForeignKey(default=1,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='rates',
                                    to='currency.source'),
            preserve_default=False,
        ),
    ]
