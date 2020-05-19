# Generated by Django 3.0.6 on 2020-05-19 14:32

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
            name='Mahasiswa',
            fields=[
                ('niu', models.IntegerField(primary_key=True, serialize=False)),
                ('nim', models.CharField(max_length=100)),
                ('nama', models.CharField(max_length=100)),
                ('program_studi', models.CharField(choices=[('Teknologi Informasi', 'Teknologi Informasi'), ('Teknik Elektro', 'Teknik Elektro'), ('Teknik Biomedis', 'Teknik Biomedis')], max_length=100)),
                ('angkatan', models.IntegerField(default=2016)),
            ],
        ),
        migrations.CreateModel(
            name='Pertemuan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intensitas', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UploadCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.IntegerField()),
                ('nama', models.CharField(max_length=100)),
                ('nim', models.IntegerField()),
                ('attendance', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deskripsi_video', models.CharField(max_length=500)),
                ('videofile', models.FileField(null=True, upload_to='video/%Y-%m-%d/', verbose_name='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=100)),
                ('nama', models.CharField(max_length=100)),
                ('ruang', models.CharField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presensi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_kehadiran', models.DateField(auto_now=True)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halaman.Mahasiswa')),
                ('pertemuan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halaman.Pertemuan')),
            ],
        ),
        migrations.AddField(
            model_name='pertemuan',
            name='matkul',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pertemuan', to='halaman.Profil'),
        ),
    ]
