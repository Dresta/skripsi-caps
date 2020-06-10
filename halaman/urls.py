from django.urls import path
from . import views


urlpatterns = [
    path('registrasi/', views.daftar, name='daftar'),
    path('dataAkun/', views.dataAkun, name='dataAkun'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('aktivitas/', views.aktivitas, name='aktivitas'),
    path('mahasiswa/', views.daftarMahasiswa, name='daftarMahasiswa'),
    path('detail/<str:pk>', views.detail, name='detail'),
    path('rekap/', views.rekap, name='rekap'),
    path('rekapDetail/<str:pk>', views.rekapDetail, name='rekapDetail'),
    path('dashboard_akademik', views.dashboard_akademik, name='Dashboard'),
    path('video/', views.video, name='video'),
    path('presensi/', views.presensi, name='presensi')
] 
