from django import forms
from halaman.models import Video, FileKehadiran

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