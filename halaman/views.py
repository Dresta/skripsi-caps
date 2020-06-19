from django.shortcuts import render, redirect
from django.http import HttpResponse

import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user

from .models import Profil, Mahasiswa, Presensi, Pertemuan, Video, UploadCSV
from .forms import PertemuanForm, ProfilForm, VideoForm, KehadiranForm

from django.core.serializers import serialize
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import *

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
    last_user = User.objects.all().last()

    if request.method == 'POST':
        data = request.POST
        last_id = last_user.pk
        profil = Profil.objects.create(
            user_id = last_id,
            kode = data['kode'],
            nama = data['matkul'],
            ruang = data['ruang'],
            jadwal = data['jadwal'])

        profil.save()
        return redirect('dashboard')
        
    context={
        'last_user' : last_user,
    }
    return render(request, 'data_akun.html', context)

@login_required(login_url='masuk')
def dashboard(request):
    # ALTER TABLE halaman_pertemuan AUTO_INCREMENT=1;
    log_user = request.user
    nama_matkul = request.user.profil
    pertemuan = Pertemuan.objects.filter(matkul__nama=nama_matkul)

    profil = Profil.objects.all()

    log_user = request.user
    nama_matkul = request.user.profil
    jumlah = Pertemuan.objects.filter(matkul__nama=nama_matkul).count

    if request.user.is_superuser:
        return redirect('Dashboard')

    else:
        if request.method == "POST": 
            if 'mulai_kuliah' in request.POST:   
                data = request.POST
                matkul_id = request.user.profil.id
                pertemuan = Pertemuan.objects.create(matkul_id=matkul_id)
                # if pertemuan:
                #     return redirect('/halaman/dashboard/')
                # else:
                #     return HttpResponse("Pertemuan tidak terselenggara")

        context = {
            'nama_matkul' : nama_matkul,
            "hal_dashboard" : "active",
            'profil' : profil, 
            'jumlah' : jumlah,
        }
        
        return render (request, 'dashboard.html', context)

@login_required(login_url='masuk')
def dashboard_akademik(request):
    profil = User.objects.exclude(groups = 1)

    context = {
        'profil' : profil ,
        "hal_dashboard_aka" : "active",
    }
    return render (request, 'dashboardAkademik.html', context)

@login_required(login_url='masuk')
def detailAkun(request, pk):
    profil = Profil.objects.get(id=pk)
    pertemuan = profil.pertemuan.all()
    jumlah = pertemuan.count()
    terakhir = pertemuan.last()

    context = {
        'profil':profil, 'pertemuan':pertemuan, 'jumlah':jumlah,
        'terakhir':terakhir,
    }
    return render(request, 'detailAkun.html', context)

@login_required(login_url='masuk')
def hapus_akun(request, pk):
    if request.method == "POST":
        akun = User.objects.get(id = pk)
        akun.delete()
    return redirect('Dashboard')

@login_required(login_url='masuk')
def aktivitas(request):
    pertemuan = Pertemuan.objects.last()

    context = {
        
   }
    return render (request, 'aktivitas.html', context)

@login_required(login_url='masuk')
def daftarMahasiswa(request):

    log_user = request.user
    nama_matkul = request.user.profil
    presensi = Presensi.objects.filter(pertemuan__matkul=nama_matkul)
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

    context = {
      "hal_daftarMahasiswa" : "active",
      'presensi': presensi, 'mahasiswa':mahasiswa,

   }
    return render(request, 'mahasiswa.html', context)

@login_required(login_url='masuk')
def detailMahasiswa(request, pk):

    log_user = request.user
    nama_matkul = request.user.profil
    list_pertemuan = Pertemuan.objects.filter(matkul=nama_matkul)
    kehadiran = Presensi.objects.filter(pertemuan__in=list_pertemuan)

    mahasiswa = Mahasiswa.objects.get(niu=pk)
    listPresensi = mahasiswa.presensi_set.all()

    selectedId = mahasiswa.presensi_set.values_list('pertemuan__matkul', flat=True).distinct()
    matkul = Profil.objects.filter(id__in = selectedId)
    presensi = Presensi.objects.filter(mahasiswa = pk)

    context = {
        'mahasiswa':mahasiswa, 'presensi':presensi, 'matkul':matkul,

    }
    return render(request, 'detailMahasiswa.html', context)

@login_required(login_url='masuk')
def detailPerkuliahan(request, niu, pk):
    mahasiswa = Mahasiswa.objects.get(niu=niu)

    profil = Profil.objects.get(id = pk)

    presensi = Presensi.objects.filter(pertemuan__matkul__id = pk).filter(mahasiswa = niu)
    jumlah = presensi.count()
    kehadiran = presensi.filter(status = 1).count()
    terakhir = presensi.filter(status = 1).last()
    batas = jumlah * 0.75

    print(presensi)
    context ={
        'mahasiswa':mahasiswa, 'profil':profil, 'presensi':presensi,
        'kehadiran':kehadiran, 'jumlah':jumlah, 'terakhir':terakhir, 'batas':batas,
    }
    return render(request, 'detailPerkuliahan.html', context)

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
    

    hadir = presensi.exclude(status="0")
    absen = presensi.filter(status="0")

    context = {
        'pertemuan':pertemuan, 'presensi':presensi,
        'hadir':hadir, 'absen':absen,
    }
    return render(request, 'rekapDetail.html', context)
    
@login_required(login_url='masuk')
def faceDetection(request):

    videos = Video.objects.all()
    hapus = UploadCSV.objects.all().delete()

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
        'hal_upload' : 'active'
    }
    return render(request, 'video.html', context)

@login_required(login_url='masuk')
def uploadKehadiran(request):
    hapus = UploadCSV.objects.all().delete()
    kehadiran = FileKehadiran.objects.all()
    if request.method == "POST":
        if 'fileKehadiran' in request.POST:
            fileKehadiran = KehadiranForm (request.POST, request.FILES)
            if fileKehadiran.is_valid():
                fileKehadiran.save()
            return redirect('script')
        # elif 'upload' in request.POST:
        #     csv_file = request.FILES.get("file", None)

        #     if not csv_file.name.endswith(".csv"):
        #         messages.error(request, 'File yang dimasukkan bukan csv')

        #     data_set = csv_file.read().decode('UTF-8')
        #     io_string = io.StringIO(data_set)
        #     next(io_string)
        #     for column in csv.reader(io_string, delimiter=",", quotechar="|"):
        #         _, created = UploadCSV.objects.get_or_create(
        #             nomor = column[0],
        #             nama = column[1],
        #             nim = column[2],
        #             attendance = column[3]
        #         )
        #     return redirect('presensi')

    else:
        fileKehadiran = KehadiranForm ()
    context ={
        'hapus' : hapus, 'fileKehadiran' : fileKehadiran, 
    }
    return render(request, 'upload.html', context)

@login_required(login_url='masuk')
def presensi(request):
    pertemuan = Pertemuan.objects.all()
    tersedia = pertemuan.filter(simpan = 0).count() 
    dummy = UploadCSV.objects.all()
    jumlah_kehadiran = dummy.count()
    hapus = UploadCSV.objects.all().delete()

    print(jumlah_kehadiran)

    if request.method == "POST":
        if "simpan" in request.POST:
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
        'hal_presensi' : 'active', 'tersedia':tersedia, 
        'jumlah_kehadiran':jumlah_kehadiran, 'hapus':hapus,

    }
    return  render(request, 'presensi.html', context  )

@login_required(login_url='masuk') 
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
        
    face_cascade = cv2.CascadeClassifier('halaman/video/haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture('halaman/video/test6.mp4') #ini harusnya bisa dibuat dinamis

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
            if confidence < 90:
                confidence = round(confidence)
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
            
    
            cv2.imshow('Face Recognizer',img)
            #k = cv2.waitKey(30) & 0xff
            if cv2.waitKey(1) == ord('a'):
            #num+=1
            #if num>200:
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

class MahasiswaViewSet(viewsets.ModelViewSet):
    queryset = Mahasiswa.objects.all().order_by('niu')
    serializer_class = MahasiswaSerializer

class PertemuanViewSet(viewsets.ModelViewSet):
    queryset = Pertemuan.objects.all().order_by('matkul')
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