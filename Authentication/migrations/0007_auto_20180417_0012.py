# Generated by Django 2.0.4 on 2018-04-16 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_auto_20180416_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='journey_date',
            field=models.DateField(verbose_name='Journey Date'),
        ),
    ]