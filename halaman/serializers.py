from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'groups']

class ProfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profil
        fields = ['id', 'kode', 'nama', 'ruang']

class MatkulSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matkul
        fields = ['id', 'user', 'profil']

class MahasiswaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['url', 'niu', 'nama', 'nim', 'angkatan', 'program_studi']


class PertemuanSerializer(serializers.ModelSerializer):
    profil = serializers.SerializerMethodField('get_profil_name')
    class Meta:
        model = Pertemuan
        fields = ['url', 'id', 'profil', 'waktu_perkuliahan', 'tanggal_perkuliahan', 'simpan',]


    def get_profil_name(self, obj):
        return obj.profil.nama


class PresensiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presensi
        fields = ['pertemuan', 'mahasiswa', 'status']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class FileKehadiranSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileKehadiran
        fields = "__all__"

class UploadCSVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadCSV
        fields = ['url', 'nim', 'nomor', 'nama', 'attendance']
        