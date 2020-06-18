# Generated by Django 3.0.6 on 2020-06-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halaman', '0015_auto_20200618_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileKehadiran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deskripsi_file', models.CharField(max_length=500)),
                ('fileKehadiran', models.FileField(null=True, upload_to='kehadiran/', verbose_name='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]