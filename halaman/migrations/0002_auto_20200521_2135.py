# Generated by Django 3.0.6 on 2020-05-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halaman', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presensi',
            name='waktu_kehadiran',
        ),
        migrations.AddField(
            model_name='pertemuan',
            name='waktu_perkuliahan',
            field=models.DateField(auto_now=True),
        ),
    ]