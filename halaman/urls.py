from django.urls import path
from . import views


urlpatterns = [
    path('dosen/', views.dosen, name="dosen"),
    path('dosen/dashboard/<str:idmatkul>', views.dashboard , name='dashboard'),
    path('dosen/rekap/<str:idmatkul>', views.rekap, name='rekap'),
    path('dosen/rekap/<str:idmatkul>/<str:pk>', views.detailRekap, name='detailRekap'),
    
    path('akademik/', views.dashboard_akademik, name='Dashboard'),
    path('akademik/registrasi/akun/', views.daftar, name='daftar'),
    path('akademik/registrasi/profil/', views.dataAkun, name='dataAkun'),
    path('akademik/registrasi/pengajar/', views.tambahPengajar, name='tambahPengajar'),
    path('akademik/matakuliah/<str:pk>', views.detailAkun, name='detailAkun'),
    path('akademik/matakuliah/delete/<str:pk>', views.hapus_akun, name='hapus_akun'),
    path('akademik/mahasiswa/', views.daftarMahasiswa, name='daftarMahasiswa'),
    path('akademik/mahasiswa/<str:pk>', views.detailMahasiswa, name='detail'),
    path('akademik/mahasiswa/<str:niu>/<str:pk>', views.detailPerkuliahan, name='detailPerkuliahan'),
    path('akademik/presensi/', views.presensi, name='presensi'),
    path('akademik/FaceDetection/', views.script, name='script'),
    path('akademik/video/', views.faceDetection, name='video'),
    path('akademik/upload/', views.uploadKehadiran, name='upload'),
] 
