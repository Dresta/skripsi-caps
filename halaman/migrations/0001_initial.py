# Generated by Django 3.0.6 on 2020-08-04 06:18

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
            name='Dummy',
            fields=[
                ('nomor', models.IntegerField()),
                ('nama', models.CharField(max_length=30)),
                ('nim', models.IntegerField(primary_key=True, serialize=False)),
                ('attendance', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileKehadiran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileKehadiran', models.FileField(null=True, upload_to='kehadiran/', verbose_name='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Mahasiswa',
            fields=[
                ('niu', models.IntegerField(primary_key=True, serialize=False)),
                ('nim', models.CharField(max_length=18)),
                ('nama', models.CharField(max_length=30)),
                ('program_studi', models.CharField(choices=[('Teknologi Informasi', 'Teknologi Informasi'), ('Teknik Elektro', 'Teknik Elektro'), ('Teknik Biomedis', 'Teknik Biomedis')], max_length=20)),
                ('angkatan', models.IntegerField(default=2016)),
            ],
        ),
        migrations.CreateModel(
            name='Matkul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=20)),
                ('nama', models.CharField(max_length=50)),
                ('ruang', models.CharField(max_length=6)),
                ('hari', models.CharField(choices=[('Senin', 'Senin'), ('Selasa', 'Selasa'), ('Rabu', 'Rabu'), ('Kamis', 'Kamis'), ('Jumat', 'Jumat')], max_length=6)),
                ('jadwal', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Pertemuan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengajar', models.CharField(max_length=6)),
                ('tanggal_perkuliahan', models.DateField(auto_now_add=True)),
                ('waktu_perkuliahan', models.TimeField(auto_now_add=True)),
                ('simpan', models.BooleanField(default=0)),
                ('matkul', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pertemuan', to='halaman.Matkul')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(null=True, upload_to='video/', verbose_name='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Presensi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=2)),
                ('mahasiswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halaman.Mahasiswa')),
                ('pertemuan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='halaman.Pertemuan')),
            ],
        ),
        migrations.CreateModel(
            name='Perkuliahan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matkul', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profil', to='halaman.Matkul')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['matkul'],
            },
        ),
    ]
