"""capstoneproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from halaman.views import masuk, keluar, UserViewSet, ProfilViewSet, MahasiswaViewSet, PertemuanViewSet, PresensiViewSet, VideoViewSet, UploadCSVViewSet

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.models import User
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profil', ProfilViewSet)
router.register('mahasiswa', MahasiswaViewSet)
router.register('pertemuan', PertemuanViewSet)
router.register('video', VideoViewSet)
router.register('upload', UploadCSVViewSet)


urlpatterns = [
    path('masuk/', masuk, name='masuk'),
    path('keluar/', keluar, name='keluar'),
    path('admin/', admin.site.urls),
    path('halaman/', include('halaman.urls')),

    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)