from django.urls import path
from . import views


urlpatterns = [
    path('registrasi/', views.daftar, name='daftar'),
    path('dataAkun/', views.dataAkun, name='dataAkun'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('aktivitas/', views.aktivitas, name='aktivitas'),
    path('mahasiswa/', views.daftarMahasiswa, name='daftarMahasiswa'),
    path('mahasiswa/<str:pk>', views.detailMahasiswa, name='detail'),
    path('mahasiswa/<str:niu>/<str:pk>', views.detailPerkuliahan, name='detailPerkuliahan'),
    path('rekap/', views.rekap, name='rekap'),
    path('rekap/<str:pk>', views.rekapDetail, name='rekapDetail'),
    path('dashboard_akademik/', views.dashboard_akademik, name='Dashboard'),
    path('dashboard_akademik/<str:pk>', views.akunDetail, name='akunDetail'),
    path('delete/id_akun/<str:pk>', views.hapus_akun, name='hapus_akun'),
    path('video/', views.video, name='video'),
    path('upload/', views.uploadKehadiran, name='upload'),
    path('presensi/', views.presensi, name='presensi'),
    path('FaceDetection/', views.faceDetection, name='script'),
] 
