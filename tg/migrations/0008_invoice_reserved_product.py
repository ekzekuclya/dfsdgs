# Generated by Django 4.2.16 on 2024-12-03 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0007_product_reserved'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='reserved_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tg.product'),
        ),
    ]
