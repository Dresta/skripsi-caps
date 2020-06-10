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
    path('video/', views.video, name='video'),
    path('kenzy/', views.kenzy, name='kenzy'),
    path('kenzy2/', views.kodeKenzy, name='script'),
    path('uploadkenzy/', views.uploadkenzy, name='uploadkenzy')
] 
