from django import forms
from halaman.models import Video, FileKehadiran, Matkul

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

class MatkulForm(forms.ModelForm):
    
    class Meta:
        model = Matkul
        fields = '__all__'

        widgets = {
            'user' : forms.Select(attrs={'class':'form-control'}),
            'profil' : forms.Select(attrs={'class':'form-control'})
        }
        # def __init__(self,matkul,*args,**kwargs):
        #     super (MatkulForm,self ).__init__(*args,**kwargs) # populates the post
        #     self.fields['user'].queryset = User.objects.filter(groups = 'dosen')