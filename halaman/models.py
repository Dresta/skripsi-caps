from django.db import models
from django.db import transaction
from django.db.models import F, Max

from django.contrib.auth.models import User

# Create your models here.
class Profil(models.Model):
    HARI=(
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
    )
    kode = models.CharField(max_length=20)
    nama = models.CharField(max_length=50)
    ruang = models.CharField(max_length=6)
    hari = models.CharField(choices=HARI, max_length=6)
    jadwal = models.TimeField()

    def __str__(self):
        return self.nama

class Matkul(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='profil')

    class Meta:
        ordering = ['profil']

    def __str__(self):
        return self.profil.nama + ' - ' + self.user.username

class Mahasiswa(models.Model):
    PRODI=(
        ('Teknologi Informasi', 'Teknologi Informasi'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Teknik Biomedis', 'Teknik Biomedis'),
    )
    niu = models.IntegerField(primary_key=True)
    nim = models.CharField(max_length=18)
    nama = models.CharField(max_length=30)
    program_studi = models.CharField(choices=PRODI, max_length=20)
    angkatan = models.IntegerField(default=2016)

    def __str__(self):
        return ' %s - %s' % ( self.niu, self.nama)

class Pertemuan(models.Model):
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='pertemuan')
    pengajar = models.CharField(max_length=6)
    tanggal_perkuliahan = models.DateField(auto_now_add=True, blank=True)
    waktu_perkuliahan = models.TimeField(auto_now_add=True, blank=True)
    simpan = models.BooleanField(default=0)

    def __str__(self):
        return 'id pertemuan %s mata kuliah %s'  % (self.id , self.profil.nama)

class Presensi(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return ' %s %s - %s' % (self.pertemuan.profil.nama,  self.pertemuan.waktu_perkuliahan, self.mahasiswa.niu) 

class Video(models.Model):
    videofile = models.FileField(upload_to='video/', null=True, verbose_name='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.videofile.name

class UploadCSV(models.Model):
    nomor = models.IntegerField()
    nama = models.CharField(max_length = 30)
    nim = models.IntegerField(primary_key=True)
    attendance = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.nim)

class FileKehadiran(models.Model):
    fileKehadiran = models.FileField(upload_to='kehadiran/', null=True, verbose_name='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.fileKehadiran.name