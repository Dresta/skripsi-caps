# Generated by Django 2.0.7 on 2020-06-10 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halaman', '0002_auto_20200610_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='videofile',
            field=models.FileField(null=True, upload_to='video/%Y-%m-%d/', verbose_name=''),
        ),
    ]
