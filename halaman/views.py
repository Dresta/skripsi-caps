from django.shortcuts import render, redirect
from django.http import HttpResponse

import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user

from .models import Profil, Mahasiswa, Presensi, Pertemuan, Video, UploadCSV
from .forms import PertemuanForm, ProfilForm, VideoForm

# Create your views here.
@unauthenticated_user
def masuk(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'username atau password anda tidak cocok')

    return render(request, 'masuk.html')

def keluar(request):
    logout(request)
    return redirect('masuk')

@login_required(login_url='masuk')
def daftar(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # nama = form.cleaned_data.get('username')
            # messages.success(request, f'Akun { nama } berhasil dibuat')
            group = Group.objects.get(name='dosen')
            user.groups.add(group)

            form = UserCreationForm()
            return redirect('dataAkun')
    else:
        form = UserCreationForm()

    context={
        "hal_daftar" : "active",
        'form' : form,
    }
    return render(request, 'register.html', context)

@login_required(login_url='masuk')
def dataAkun(request):
    dataform = ProfilForm(request.POST)

    if request.method == 'POST':
        dataform = ProfilForm(request.POST)
        if dataform.is_valid():
            dataform.save()
            
            dataform = ProfilForm()
            return redirect('daftar')
    else:
        dataform = ProfilForm()
        
    context={
        'dataform' : dataform,
    }
    return render(request, 'data_akun.html', context)

@login_required(login_url='masuk')
def dashboard(request):
    # ALTER TABLE halaman_pertemuan AUTO_INCREMENT=1;
    log_user = request.user
    nama_matkul = request.user.profil
    pertemuan = Pertemuan.objects.filter(matkul__nama=nama_matkul)

    profil = Profil.objects.all()

    if request.method == "POST":    
        form_pertemuan = PertemuanForm(request.POST)
        if form_pertemuan.is_valid():
            n = form_pertemuan.cleaned_data["matkul"]
            t = Pertemuan (matkul = n)
            t.save()
            request.user.profil.pertemuan.add(t)

            return redirect('aktivitas')
    else:
        form_pertemuan = PertemuanForm()

    context = {
        'nama_matkul' : nama_matkul,
        "hal_dashboard" : "active",
        'profil' : profil, 
        'form_pertemuan':form_pertemuan,
    }
    return render (request, 'dashboard.html', context)
    
@login_required(login_url='masuk')
def aktivitas(request):
    pertemuan = Pertemuan.objects.last()

    if request.method == 'GET':
        #if mahasiswa.niu == json.niu -> tampilkan nama || get
        pass
    elif request.method == 'POST':
        #if button clicked -> save  to db || post
        pass

    context = {
        
   }
    return render (request, 'aktivitas.html', context)

@login_required(login_url='masuk')
def daftarMahasiswa(request):
    
    mahasiswa = Mahasiswa.objects.all()
    presensi = Presensi.objects.all()

    context = {
      "hal_daftarMahasiswa" : "active",
      "mahasiswa" : mahasiswa, 'presensi': presensi,

   }
    return render(request, 'mahasiswa.html', context)

@login_required(login_url='masuk')
def detail(request, pk):
    mahasiswa = Mahasiswa.objects.get(niu=pk)
    presensi = mahasiswa.presensi_set.all()

    jumlah_hadir = presensi.filter(status="Hadir").count()
    jumlah_terlambat = presensi.filter(status="Telat").count()
    jumlah_absen = presensi.filter(status="Absen").count()
    total_kehadiran = presensi.exclude(status="Absen").count()

    context = {
        'mahasiswa':mahasiswa, 'presensi':presensi,
        'jumlah_hadir' :jumlah_hadir, 'jumlah_terlambat':jumlah_terlambat, 
        'jumlah_absen':jumlah_absen, 'total_kehadiran':total_kehadiran,
    }
    return render(request, 'detail.html', context)

@login_required(login_url='masuk')
def rekap(request):
    log_user = request.user
    nama_matkul = request.user.profil
    pertemuan = Pertemuan.objects.filter(matkul__nama=nama_matkul)

    presensi = Presensi.objects.all()

    jumlah_hadir = presensi.exclude(status="Absen").count()

    context = {
        "hal_rekap" : "active",
        'presensi':presensi, 'pertemuan':pertemuan, 'jumlah_hadir':jumlah_hadir,
    }
    return render(request, 'rekap.html', context)

@login_required(login_url='masuk')
def rekapDetail(request, pk):
    pertemuan = Pertemuan.objects.get(id=pk)
    presensi = Presensi.objects.filter(pertemuan_id = pk)

    hadir = presensi.exclude(status="Absen")
    absen = presensi.filter(status="Absen")

    context = {
        'pertemuan':pertemuan, 'presensi':presensi,
        'hadir':hadir, 'absen':absen,
    }
    return render(request, 'rekapDetail.html', context)
    

def video(request):

    videos = Video.objects.all()

    if request.method == "POST":
        csv_file = request.FILES.get("file", None)

        if not csv_file.name.endswith(".csv"):
            messages.error(request, 'File yang dimasukkan bukan csv')
        
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=",", quotechar="|"):
            _, created = UploadCSV.objects.get_or_create(
                nomor = column[0],
                nama = column[1],
                nim = column[2],
                attendance = column[3]
            )

        form = VideoForm (request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = VideoForm()
    
    # if request.method == "GET":
    #     return render(request, 'video.html')

    # csv_file = request.FILES.get("file", None)

    # if not csv_file.name.endswith(".csv"):
    #     messages.error(request, 'File yang dimasukkan bukan csv')
    
    # data_set = csv_file.read().decode('UTF-8')
    # io_string = io.StringIO(data_set)
    # next(io_string)
    # for column in csv.reader(io_string, delimiter=",", quotechar="|"):
    #     _, created = UploadCSV.objects.get_or_create(
    #         nomor = column[0],
    #         nama = column[1],
    #         nim = column[2],
    #         attendance = column[3]
    #     )

    context={
        'form':form, 'videos':videos
    }
    return render(request, 'video.html', context)

# def uploadCSV(request):
#     template = 'video.html'
#     prompt ={
#         'order' : 'order of CSV should be nomor, nama, nim, attendance'
#     }

#     if request.method == "GET":
#         return render(request, template, prompt)

#     csv_file = request.FILES.get("file", None)

#     if not csv_file.name.endswith(".csv"):
#         messages.error(request, 'File yang dimasukkan bukan csv')
    
#     data_set = csv_file.read().decode('UTF-8')
#     io_string = io.StringIO(data_set)
#     next(io_string)
#     for column in csv.reader(io_string, delimiter=",", quotechar="|"):
#         _, created = UploadCSV.objects.update_or_create(
#             nomor = column[0],
#             nama = column[1],
#             nim = column[2],
#             attendance = column[3]
#         )
#     return render (request, 'video.html', context)

def kodeKenzy(request):
    #masukkan kode kenzy
    pass

    return render (request, 'video.html', context)