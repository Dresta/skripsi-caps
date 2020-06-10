from django.db import models
from django.db import transaction
from django.db.models import F, Max

from django.contrib.auth.models import User

# Create your models here.
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    kode = models.CharField(max_length=100)
    nama = models.CharField(max_length=100)
    ruang = models.CharField(max_length=6)
    jadwal = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.nama

class Mahasiswa(models.Model):
    PRODI=(
        ('Teknologi Informasi', 'Teknologi Informasi'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Teknik Biomedis', 'Teknik Biomedis'),
    )
    niu = models.IntegerField(primary_key=True)
    nim = models.CharField(max_length=100)
    nama = models.CharField(max_length=100)
    program_studi = models.CharField(choices=PRODI, max_length=100)
    angkatan = models.IntegerField(default=2016)

    def __str__(self):
        return ' %s - %s' % ( self.niu, self.nama)

class Pertemuan(models.Model):
    matkul = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='pertemuan')
    waktu_perkuliahan = models.DateField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        self.intensitas = Pertemuan.objects.count()
        super(Pertemuan, self).save(*args, **kwargs)

    def __str__(self):
        return 'id pertemuan %s mata kuliah %s'  % (self.id , self.matkul.nama)

class Presensi(models.Model):
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return ' Pertemuan %s %s - %s' % ( self.pertemuan.id, self.pertemuan.matkul.nama, self.mahasiswa.niu) 

class Video(models.Model):
    deskripsi_video = models.CharField(max_length=500)
    videofile = models.FileField(upload_to='video/%Y-%m-%d/', null=True, verbose_name='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.deskripsi_video

class UploadCSV(models.Model):
    nomor = models.IntegerField()
    nama = models.CharField(max_length = 100)
    nim = models.IntegerField(primary_key=True)
    attendance = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.nim)