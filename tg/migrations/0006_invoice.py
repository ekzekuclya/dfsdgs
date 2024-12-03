# Generated by Django 4.2.16 on 2024-12-03 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0005_chapter_alter_product_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('req', models.TextField()),
                ('ltc_sum', models.FloatField()),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg.telegramuser')),
            ],
        ),
    ]
