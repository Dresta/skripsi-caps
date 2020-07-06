from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Matkul)
admin.site.register(Mahasiswa)
admin.site.register(Perkuliahan)
admin.site.register(Pertemuan)
admin.site.register(Presensi)
admin.site.register(Dummy)
admin.site.register(Video)
admin.site.register(FileKehadiran)