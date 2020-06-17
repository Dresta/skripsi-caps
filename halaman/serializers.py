from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'groups']

class ProfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profil
        fields = ['user', 'id', 'kode', 'nama', 'ruang']

class MahasiswaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['url', 'niu', 'nama', 'nim', 'angkatan', 'program_studi']


class PertemuanSerializer(serializers.ModelSerializer):
    nama_matkul = serializers.SerializerMethodField('get_matkul_name')
    class Meta:
        model = Pertemuan
        fields = ['url', 'id', 'nama_matkul', 'waktu_perkuliahan', 'tanggal_perkuliahan', 'simpan',]


    def get_matkul_name(self, obj):
        return obj.matkul.nama


class PresensiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presensi
        fields = ['pertemuan', 'mahasiswa', 'status']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class UploadCSVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadCSV
        fields = ['url', 'nim', 'nomor', 'nama', 'attendance']
        