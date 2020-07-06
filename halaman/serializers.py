from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'groups']

class MatkulSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matkul
        fields = ['id', 'kode', 'nama', 'ruang']

class PerkuliahanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Perkuliahan
        fields = ['id', 'user', 'matkul']

class MahasiswaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['url', 'niu', 'nama', 'nim', 'angkatan', 'program_studi']


class PertemuanSerializer(serializers.ModelSerializer):
    matkul = serializers.SerializerMethodField('get_matkul_name')
    class Meta:
        model = Pertemuan
        fields = ['url', 'id', 'matkul', 'waktu_perkuliahan', 'tanggal_perkuliahan', 'simpan',]


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

class FileKehadiranSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileKehadiran
        fields = "__all__"

class DummySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ['url', 'nim', 'nomor', 'nama', 'attendance']
        