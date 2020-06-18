from django import forms
from halaman.models import Pertemuan, Profil, Video, FileKehadiran

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
        self.fields['jadwal'].label = 'Jadwa Perkuliahan'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

        widgets = {
            'videofile' : forms.FileInput(attrs={'class':'upload'})
        }

class KehadiranForm(forms.ModelForm):
    class Meta:
        model = FileKehadiran
        fields = '__all__'