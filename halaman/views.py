from django.shortcuts import render, redirect
from django.http import HttpResponse

import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user, allowed_users

from .models import *
from .forms import *
from .serializers import *

from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core.serializers import serialize


# Create your views here.
@unauthenticated_user
def masuk(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboardDosen')
        else:
            messages.warning(request, 'username atau password anda tidak cocok')

    return render(request, 'masuk.html')

def keluar(request):
    logout(request)
    return redirect('masuk')


def dashboardDosen(request):

    log_user = request.user
    matkul = Matkul.objects.filter( user_id = log_user )

    if request.user.is_staff:
        return redirect('Dashboard')

    else:

        context = {
            'matkul' : matkul,
        }
        return render (request, 'dashboardDosen.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['dosen'])
def perkuliahan(request, idmatkul):

    log_user = request.user
    matkul = Matkul.objects.get(id = idmatkul)

    nama_matkul = matkul.profil
    pertemuan = Pertemuan.objects.filter(profil__nama = nama_matkul)
    profil = Profil.objects.all()

    jumlah = Pertemuan.objects.filter(profil__nama = nama_matkul).count

    if request.method == "POST": 
        if 'mulai_kuliah' in request.POST:   
            data = request.POST
            profil_id = matkul.profil.id
            pertemuan = Pertemuan.objects.create(
                profil_id = profil_id,
                pengajar = log_user,
                )
            messages.success(request, 'Pertemuan berhasil dilaksanakan')

    context = {
        'nama_matkul' : nama_matkul,
        "hal_dashboard" : "actives",
        'profil' : profil, 
        'jumlah' : jumlah,
        'matkul' :matkul,
    }
        
    return render (request, 'perkuliahan.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['dosen'])
def rekap(request, idmatkul):
    matkul = Matkul.objects.get(id = idmatkul)

    nama_matkul = matkul.profil
    pertemuan = Pertemuan.objects.filter(profil__nama = nama_matkul)

    presensi = Presensi.objects.all()

    jumlah_hadir = presensi.exclude(status="Absen").count()

    context = {
        "hal_rekap" : "actives", 'matkul' : matkul,
        'presensi':presensi, 'pertemuan':pertemuan, 'jumlah_hadir':jumlah_hadir,
    }
    return render(request, 'rekap.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['dosen'])
def detailRekap(request, idmatkul, pk):
    matkul = Matkul.objects.get(id = idmatkul)
    pertemuan = Pertemuan.objects.get(id = pk)
    presensi = Presensi.objects.filter(pertemuan_id = pk)
    
    hadir = presensi.exclude(status = "0")
    absen = presensi.filter(status = "0")

    context = {
        'pertemuan':pertemuan, 'presensi':presensi,
        'hadir':hadir, 'absen':absen, 'matkul':matkul,
    }
    return render(request, 'detailRekap.html', context)

#akademik
@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def dashboardAkademik(request):
    grup = Group.objects.get(name='dosen')
    grupDosen = User.objects.filter(groups = grup)
    
    matkul = Matkul.objects.filter(user__in = grupDosen)
    profil = Profil.objects.all()
    
    context = {
        'matkul' : matkul , 'profil' : profil, 'dosen': grupDosen, 
        "hal_dashboard_aka" : "actives",
    }
    return render (request, 'dashboardAkademik.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def tambahMatkul(request):

    if request.method == 'POST':
        data = request.POST
        profil = Profil.objects.create(
            kode = data['kode'],
            nama = data['matkul'],
            ruang = data['ruang'],
            hari = data['hari'],
            jadwal = data['jadwal'])

        profil.save()
        messages.success(request, 'Mata kuliah telah berhasil dibuat')
        return redirect('Dashboard')
        
    context={
    }
    return render(request, 'tambahMatkul.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def tambahDosen(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        data = request.POST
        if data['password1'] == data['password2']:

            user = User.objects.create_user(
                username = data['username'],
                password = data['password1'],
            )
            user.first_name = data['nama_awal']
            user.last_name = data['nama_akhir']
            user.save() 
            messages.success(request, 'Akun dosen telah berhasil dibuat')
            group = Group.objects.get(name='dosen')
            user.groups.add(group)
            return redirect('Dashboard')
        else:
            messages.warning(request, 'Password tidak sesuai')
            return redirect('tambahDosen')

    context={
        "hal_daftar" : "actives",
        'form' : form,
    }
    return render(request, 'tambahDosen.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def tambahPengajar(request):
    grup = Group.objects.get(name='akademik')

    akun = User.objects.exclude(groups = grup)
    profil = Profil.objects.all()

    if request.method == 'POST':
        data = request.POST
        matkul = Matkul.objects.create(
            user_id = data['akun_dosen'],
            profil_id = data['matakuliah']
            )
        matkul.save()
        messages.success(request, 'Perkuliahan dapat dilakukan oleh username {0}' .format(matkul.user))
        return redirect('Dashboard')
    context = {
        'akun':akun, 'profil':profil, 
    }
    return render (request, 'tambahPengajar.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def detailDosen(request, pk):
    akun = User.objects.get(id=pk)
    matkul = Matkul.objects.filter( user=akun )

    context={
        'akun':akun, 'matkul':matkul,
    }
    return render(request, 'detailDosen.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def detailMatkul(request, pk):
    profil = Profil.objects.get(id=pk)
    matkul = Matkul.objects.filter(profil = profil)
    pertemuan = profil.pertemuan.all()
    jumlah = pertemuan.count()
    terakhir = pertemuan.last()
    pengajar = Pertemuan.objects.filter(pengajar = profil)

    context = {
        'profil':profil, 'pertemuan':pertemuan, 'jumlah':jumlah,
        'terakhir':terakhir, 'matkul':matkul, 'pengajar':pengajar,
    }
    return render(request, 'detailMatkul.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def hapus_akun(request, pk):
    if request.method == "POST":
        user = User.objects.get(id = pk)
        user.delete()
    return redirect('Dashboard')

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def hapus_matkul(request, pk):
    if request.method == "POST":
        profil = Profil.objects.get(id = pk)
        profil.delete()
    return redirect('Dashboard')

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def hapus_mahasiswa(request, niu):
    if request.method == "POST":
        mahasiswa = Mahasiswa.objects.get(niu = niu)
        mahasiswa.delete()
    return redirect('daftarMahasiswa')

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def daftarMahasiswa(request):

    mahasiswa = Mahasiswa.objects.all()
    
    if request.method == "POST":
        if 'tambah_mhs' in request.POST:   
            csv_file = request.FILES.get("file", None)

            if not csv_file.name.endswith(".csv"):
                messages.error(request, 'File yang dimasukkan bukan csv')
            
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=",", quotechar="|"):
                _, created = Mahasiswa.objects.get_or_create(
                    niu = column[0], 
                    nim = column[1],
                    nama = column[2],
                    program_studi = column[3],
                    angkatan = column[4],
                )
            messages.success(request, 'Mahasiswa berhasil ditambahkan')

    context = {
      "hal_daftarMahasiswa" : "actives", 'mahasiswa':mahasiswa,

   }
    return render(request, 'mahasiswa.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def detailMahasiswa(request, pk):

    profil = Profil.objects.all()
    list_pertemuan = Pertemuan.objects.filter(profil__in =profil)
    kehadiran = Presensi.objects.filter(pertemuan__in=list_pertemuan)

    mahasiswa = Mahasiswa.objects.get(niu=pk)
    listPresensi = mahasiswa.presensi_set.all()

    selectedId = mahasiswa.presensi_set.values_list('pertemuan__profil', flat=True).distinct()
    matkul = Profil.objects.filter(id__in = selectedId)
    presensi = Presensi.objects.filter(mahasiswa = pk)

    context = {
        'mahasiswa':mahasiswa, 'presensi':presensi, 'matkul':matkul,

    }
    return render(request, 'detailMahasiswa.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def detailPerkuliahan(request, niu, pk):
    mahasiswa = Mahasiswa.objects.get(niu=niu)

    profil = Profil.objects.get(id = pk)

    presensi = Presensi.objects.filter(pertemuan__profil__id = pk).filter(mahasiswa = niu)
    jumlah = presensi.count()
    kehadiran = presensi.filter(status = 1).count()
    terakhir = presensi.filter(status = 1).last()
    batas = jumlah * 0.75

    context ={
        'mahasiswa':mahasiswa, 'profil':profil, 'presensi':presensi,
        'kehadiran':kehadiran, 'jumlah':jumlah, 'terakhir':terakhir, 'batas':batas,
    }
    return render(request, 'detailPerkuliahan.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def faceDetection(request):

    videos = Video.objects.all()

    if request.method == "POST":
        form = VideoForm (request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload')
    else:
        form = VideoForm()
    
    context={
        'form':form, 
        'videos':videos, 
        'hal_upload' : 'actives'
    }
    return render(request, 'video.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def uploadKehadiran(request):
    hapus = UploadCSV.objects.all().delete()
    kehadiran = FileKehadiran.objects.all()
    if request.method == "POST":
        if 'fileKehadiran' in request.POST:
            fileKehadiran = KehadiranForm (request.POST, request.FILES)
            if fileKehadiran.is_valid():
                fileKehadiran.save()
            return redirect('script')

    else:
        fileKehadiran = KehadiranForm ()
    context ={
        'hapus' : hapus, 'fileKehadiran' : fileKehadiran, 
    }
    return render(request, 'upload.html', context)

@login_required(login_url='masuk')
@allowed_users(allowed_roles=['akademik'])
def presensi(request):
    pertemuan = Pertemuan.objects.all()
    tersedia = pertemuan.filter(simpan = 0).count() 
    
    hapus = UploadCSV.objects.all().delete()

    if request.method == "POST":
        if "simpan" in request.POST:
            messages.success(request, 'Presensi mahasiswa berhasil disimpan')
            return redirect('daftarMahasiswa')
        if "kehadiran" in request.POST:
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
    context={
        'hal_presensi' : 'actives', 'tersedia':tersedia, 'hapus':hapus,
    }
    return  render(request, 'presensi.html', context  )

@login_required(login_url='masuk') 
@allowed_users(allowed_roles=['akademik'])
def script(request): 
    import numpy as np
    import pandas as pd
    import os
    import csv
    import cv2
    import datetime
    import json
    from time import sleep
    from openpyxl.reader.excel import load_workbook

    fname = 'halaman/video/2020-06-02/trainingData.yml'
    if not os.path.isfile(fname):
        print('first train the data')
        exit(0)

    names = {}
    labels = []
    students = []

    def getdata():
        with open('halaman/video/2020-06-02/data.csv','r') as f:
            data = csv.reader(f)
            next(data)
            lines = list(data)
            for line in lines:
                names[int(line[0])] = line[1] 

    def  markPresent(name):
        with open('halaman/video/2020-06-02/data.csv','r') as f:
            data = csv.reader(f)
            lines = list(data)
            for line in lines:
                if line[1] == name:
                    line[-1] = '1'
                    with open('halaman/video/2020-06-02/data_upload.csv','w') as g:
                        writer = csv.writer(g,lineterminator='\n')
                        writer.writerows(lines)
                        break

    def update_Excel():
        with open('halaman/video/2020-06-02/data_upload.csv') as f:
            data = csv.reader(f)
            lines = list(data)
            for line in lines:
                line.pop(0)
            with open('halaman/video/2020-06-02/data_upload.csv','w') as g:
                writer = csv.writer(g,lineterminator='\n')
                writer.writerows(lines)
                
        df = pd.read_csv('halaman/video/2020-06-02/data_upload.csv')

    def csv_to_json():
        csvfile = open('halaman/video/2020-06-02/data_upload.csv', 'r')
        jsonfile = open('halaman/video/2020-06-02/data.json', 'w')

        my_list = []
        with open('halaman/video/2020-06-02/data_upload.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["Name"]
                nim = row["NIM"]
                attendance = row["Attendance"]
                my_dict = {"Name":name, "NIM":nim, "Attendance":attendance}   
                my_list.append(my_dict)

        with open('halaman/video/2020-06-02/data.json', 'w') as outfile:
            json.dump(my_list, outfile, indent= 4)
        
    url = 'halaman/video/test6.mp4'
    face_cascade = cv2.CascadeClassifier('halaman/video/haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(url) #ini harusnya bisa dibuat dinamis

    #from_excel_to_csv() # converting the excel to csv for use
    getdata() # getting the data from csv in a dictionary
    print('Total students :',names)

    recognizer = cv2.face.LBPHFaceRecognizer_create() #LOCAL BINARY PATTERNS HISTOGRAMS Face Recognizer

    recognizer.read(fname) # read the trained yml file
    
    num=0
    while True:   
        ret, img = cap.read()
        num+=1
        if num == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray) 
        final = cv2.medianBlur(equ, 3)

        faces = face_cascade.detectMultiScale(final, 1.3, 5)
        

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            label,confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print('label:',label)
            print('confidence:',confidence)
            predicted_name = names[label]
            if confidence < 120:
                confidence = 100 - round(confidence)/3
                cv2.putText(img, predicted_name +str(confidence) +'%', (x+2,y+h-4), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
                labels.append(label)
                students.append(names[label])
                totalstudents = set(students)
                justlabels = set(labels)
                print('student Recognised : ',totalstudents,justlabels)
                for i in justlabels:
                    if labels.count(i)>10:
                        markPresent(names[label])
                        csv_to_json()
            else:
                confidence = 100 - round(confidence) / 2
                cv2.putText(img, "unknown" , (x+2,y+h-4), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
                labels.append(label)
                students.append(names[label])
                totalstudents = set(students)
                justlabels = set(labels)
                print('student Recognised : ',totalstudents,justlabels)
            
    
            cv2.imshow('Face Recognizer',img)
            #k = cv2.waitKey(30) & 0xff
            if cv2.waitKey(1) == ord('a'):
                cap.release()
                sleep(4)
                print('we are done!')
                y=json.dumps(students)
                print(y)
                update_Excel()
                break
            # else:
            #     cap.release()
                
    # cv2.destroyAllWindows()

    pass
    return redirect ('upload')



#views untuk Django Rest Framework
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer

class ProfilViewSet(viewsets.ModelViewSet):
    queryset = Profil.objects.all().order_by('id')
    serializer_class = ProfilSerializer

class MatkulViewSet(viewsets.ModelViewSet):
    queryset = Matkul.objects.all().order_by('id')
    serializer_class = MatkulSerializer

class MahasiswaViewSet(viewsets.ModelViewSet):
    queryset = Mahasiswa.objects.all().order_by('niu')
    serializer_class = MahasiswaSerializer

class PertemuanViewSet(viewsets.ModelViewSet):
    queryset = Pertemuan.objects.all().order_by('profil')
    serializer_class = PertemuanSerializer

class PresensiViewSet(viewsets.ModelViewSet):
    queryset = Presensi.objects.all().order_by('pertemuan')
    serializer_class = PresensiSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('timestamp')
    serializer_class = VideoSerializer

class FileKehadiranViewSet(viewsets.ModelViewSet):
    queryset = FileKehadiran.objects.all().order_by('timestamp')
    serializer_class = FileKehadiranSerializer

class UploadCSVViewSet(viewsets.ModelViewSet):
    queryset = UploadCSV.objects.all()
    serializer_class = UploadCSVSerializer