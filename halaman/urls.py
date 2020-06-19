from django.urls import path
from . import views


urlpatterns = [
    path('registrasi/', views.daftar, name='daftar'),
    path('dataAkun/', views.dataAkun, name='dataAkun'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('mahasiswa/', views.daftarMahasiswa, name='daftarMahasiswa'),
    path('mahasiswa/<str:pk>', views.detailMahasiswa, name='detail'),
    path('mahasiswa/<str:niu>/<str:pk>', views.detailPerkuliahan, name='detailPerkuliahan'),
    path('rekap/', views.rekap, name='rekap'),
    path('rekap/<str:pk>', views.detailRekap, name='detailRekap'),
    path('dashboard_akademik/', views.dashboard_akademik, name='Dashboard'),
    path('matakuliah/<str:pk>', views.detailAkun, name='detailAkun'),
    path('delete/id_akun/<str:pk>', views.hapus_akun, name='hapus_akun'),
    path('video/', views.faceDetection, name='video'),
    path('upload/', views.uploadKehadiran, name='upload'),
    path('presensi/', views.presensi, name='presensi'),
    path('FaceDetection/', views.script, name='script'),
    path('coba/', views.coba, name ='coba'),
] 
