# Generated by Django 3.0.6 on 2020-06-18 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halaman', '0014_auto_20200617_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pertemuan',
            name='tanggal_perkuliahan',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pertemuan',
            name='waktu_perkuliahan',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
