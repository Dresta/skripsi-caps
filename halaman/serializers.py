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
        fields = ['user', 'kode', 'nama', 'ruang']

class MahasiswaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = "__all__"

class PertemuanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pertemuan
        fields = "__all__"

class PresensiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Presensi
        fields = ['mahasiswa', 'pertemuan', 'waktu_kehadiran', 'status']

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class UploadCSVSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadCSV
        fields = "__all__"
        