# Generated by Django 3.0.6 on 2020-06-15 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('halaman', '0010_auto_20200614_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='deskripsi_video',
        ),
    ]