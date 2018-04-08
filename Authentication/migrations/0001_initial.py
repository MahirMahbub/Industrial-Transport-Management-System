# Generated by Django 2.0.4 on 2018-04-08 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(default='Dhaka', max_length=200)),
                ('sub_distict', models.CharField(default='Dhaka', max_length=200)),
                ('city', models.CharField(default='Dhaka', max_length=200)),
                ('zip', models.IntegerField(default=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current', to='Authentication.Address')),
                ('permanent_address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='permanent', to='Authentication.Address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_no', models.CharField(max_length=200)),
                ('chassis_no', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name='Vehicle Add Date')),
                ('journey_date', models.DateTimeField(verbose_name='Journey Date')),
                ('capacity', models.FloatField(default=0.0)),
                ('model', models.CharField(max_length=200)),
                ('start_price', models.IntegerField(default=0.0)),
            ],
        ),
    ]
