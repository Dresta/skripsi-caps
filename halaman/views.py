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

def kenzy(request):

    return render(request, 'kenzy.html')

def kodeKenzy(request):
    #masukkan kode kenzy
    import numpy as np
    import pandas as pd
    import os
    import csv
    import cv2
    import datetime
    import json
    from time import sleep
    from openpyxl.reader.excel import load_workbook


    #filename = '../data/Attendance_xlsx/third_year_5sem_IT2.xlsx'

    fname = 'halaman/video/2020-06-02/trainingData.yml'
    if not os.path.isfile(fname):
        print('first train the data')
        exit(0)


    names = {}
    labels = []
    students = []


    # def from_excel_to_csv():
    #     df = pd.read_excel(filename,index=False)
    #     df.to_csv('../data.csv')

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
            # for line in lines:
            #     line.pop(0)
            # print(lines)
            for line in lines:
                if line[1] == name:
                    line[-1] = '1'
                    with open('halaman/video/2020-06-02/data.csv','w') as g:
                        writer = csv.writer(g,lineterminator='\n')
                        writer.writerows(lines)
                        break


        
        # df = pd.read_csv('data.csv')
        # df.to_excel('data.xlsx',index=False)

    def update_Excel():
        with open('halaman/video/2020-06-02/data.csv.csv') as f:
            data = csv.reader(f)
            lines = list(data)
            for line in lines:
                line.pop(0)
            with open('halaman/video/2020-06-02/data.csv','w') as g:
                writer = csv.writer(g,lineterminator='\n')
                writer.writerows(lines)
                
        df = pd.read_csv('halaman/video/2020-06-02/data.csv.csv')
        #df.to_excel('../data.xlsx',index = False)

    def csv_to_json():
        csvfile = open('halaman/video/2020-06-02/data.csv', 'r')
        jsonfile = open('halaman/video/2020-06-02/data.json', 'w')

        my_list = []
        with open('halaman/video/2020-06-02/data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["Name"]
                nim = row["NIM"]
                attendance = row["Attendance"]
                my_dict = {"Name":name, "NIM":nim, "Attendance":attendance}   
                my_list.append(my_dict)

        with open('halaman/video/2020-06-02/data.json', 'w') as outfile:
            json.dump(my_list, outfile, indent= 4)
        
    # def insertdate():
    #     flag=0
    #     for i in D.filterdates():
    #         if str(i.day) == str(datetime.datetime.today().day) and str(i.month) == str(datetime.datetime.today().month) and str(i.year) == str(datetime.datetime.today().year):
    #             flag=1
    #     if flag==1:
    #         wb = load_workbook('../data/Attendance_xlsx/third_year_5sem_IT2.xlsx')
    #         print('Date:',str(i)[:11],' is written in excel and is a working day')
    #         sheet = wb.active
    #         current_row = sheet.max_row 
    #         current_column = sheet.max_column
    #         print(current_column)
    #         sheet.column_dimensions['A'].width = 20
    #         sheet.column_dimensions['B'].width = 20
    #         sheet.cell(row=1, column=1).value = "Name"
    #         sheet.cell(row=1, column=2).value = "Enrollment"


    #         current_row = sheet.max_row
    #         current_column = sheet.max_column
    #         #sheet.cell(row=1,column=current_column).width = 20
    #         sheet.cell(row=1, column=current_column+1).value = "".join(str(datetime.datetime.today())[:11])
            
    #         # save the file 
    #         wb.save('../data/Attendance_xlsx/third_year_5sem_IT2.xlsx') 
        
    #     else:
    #         print("this is a holiday popup..ask if they want to continue..")



    face_cascade = cv2.CascadeClassifier('halaman/video/haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture('halaman/video/2020-06-02/test5.mp4')

    # cap.set(3,640) # set Width
    # cap.set(4,480) # set Height

    #from_excel_to_csv() # converting the excel to csv for use
    getdata() # getting the data from csv in a dictionary
    print('Total students :',names)

    recognizer = cv2.face.LBPHFaceRecognizer_create() #LOCAL BINARY PATTERNS HISTOGRAMS Face Recognizer

    recognizer.read(fname) # read the trained yml file

    num=0
    while True:   
        ret, img = cap.read()
        #img = cv2.flip(img, -1)
        #img = cv2.rotate(img, rotateCode=cv2.ROTATE_90_CLOCKWISE)
        #img = cv2.rotate(img, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
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
            k = cv2.waitKey(30) & 0xff
            # if cv2.waitKey(33) == ord('a'):
            num+=1
            if num>200:
                cap.release()
                sleep(4)
                print('we are done!')
                y=json.dumps(students)
                print(y)
                update_Excel()
                break
        



    #cv2.destroyAllWindows()


    pass

    return render (request, 'kenzy.html', context)