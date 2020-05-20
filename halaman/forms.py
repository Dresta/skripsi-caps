from django import forms
from halaman.models import Pertemuan, Profil, Video

class PertemuanForm(forms.ModelForm):
    class Meta:
        model = Pertemuan
        fields = ['matkul',]

    def __init__(self, *args , **kwargs): 
        super(PertemuanForm, self).__init__(**kwargs)
        self.fields['matkul'].label = ''

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        exclude = ('user',)
    
    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        # self.fields['user'].label = 'Nama Akun Dosen'
        self.fields['kode'].label = 'Kode Matakuliah'
        self.fields['nama'].label = 'Nama Matakuliah'
        self.fields['ruang'].label = 'Ruang Kuliah'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'