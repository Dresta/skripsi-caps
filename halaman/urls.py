from django.urls import path
from . import views


urlpatterns = [
    path('dosen/', views.dashboardDosen, name="dashboardDosen"),
    path('dosen/perkuliahan/<str:idmatkul>', views.perkuliahan , name='perkuliahan'),
    path('dosen/rekap/<str:idmatkul>', views.rekap, name='rekap'),
    path('dosen/rekap/<str:idmatkul>/<str:pk>', views.detailRekap, name='detailRekap'),
    
    path('akademik/', views.dashboardAkademik, name='Dashboard'),
    path('akademik/registrasi/akun/', views.tambahDosen, name='tambahDosen'),
    path('akademik/registrasi/Matkul/', views.tambahMatkul, name='tambahMatkul'),
    path('akademik/registrasi/pengajar/', views.tambahPengajar, name='tambahPengajar'),
    path('akademik/Dosen/<str:pk>', views.detailDosen, name='detailDosen'),
    path('akademik/matakuliah/<str:pk>', views.detailMatkul, name='detailMatkul'),
    path('akademik/mahasiswa/', views.daftarMahasiswa, name='daftarMahasiswa'),
    path('akademik/mahasiswa/<str:pk>', views.detailMahasiswa, name='detail'),
    path('akademik/mahasiswa/<str:niu>/<str:pk>', views.detailPerkuliahan, name='detailPerkuliahan'),
    path('akademik/presensi/', views.presensi, name='presensi'),
    path('akademik/FaceDetection/', views.script, name='script'),
    path('akademik/video/', views.faceDetection, name='video'),
    path('akademik/upload/', views.uploadKehadiran, name='upload'),
    
    path('/akademik/dosen/delete/<str:pk>', views.hapus_akun, name='hapus_akun'),
    path('/akademik/matakuliah/delete/<str:pk>', views.hapus_matkul, name='hapus_matkul'),
    path('/akademik/mahasiswa/delete/<str:niu>', views.hapus_mahasiswa, name='hapus_mahasiswa'),
] 
