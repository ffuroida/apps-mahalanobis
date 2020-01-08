from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from anomalydetection.forms.views import MahalanobisCreateForm
import json, csv, re, time, os
from datetime import datetime
from anomalydetection.settings import DATA_DIR


#method view

# def index(request):

#     if request.method == "POST":
#         form = MahalanobisCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(request.FILES['nama'])
#     return render(request, 'base/mahalanobis/chart.html', {'form':MahalanobisCreateForm})

def insert(request):
    class Data:
        def __init__(self, time, abpmean, hr, pulse, resp, spo2, kelas):
            self.time = time
            self.abpmean = abpmean
            self.hr = hr
            self.pulse = pulse
            self.resp = resp
            self.spo2 = spo2
            self.kelas = kelas

    datay = []        
    abpmean = []
    hr = []
    pulse = []
    resp = []
    spo2 = []

    if request.method == 'POST':        
        for row in request.FILES['docfile']:
            data = str(row)                        
            data = data.strip("b'")
            # data = data.strip()            
            data = list(data.split(","))
            temp = {"time":data[0],"abpmean":data[1],"hr":data[2],"pulse":data[3],"resp":data[4],"spo2":data[5],"kelas":data[6].replace("\r\n","")}
            datay.append({"s1":data[0].replace('"','').replace("'",""),"s2":data[1],"s3":data[2], "s4":data[3], "s5":data[4], "s6":data[5],"s7":data[6].replace('\\r\\n"','') }) #Cara 1
            datay.append(temp)                     
            times = data[0].replace('"','').replace("'","")
            times = datetime.strptime(times, "%H:%M:%S %d/%m/%Y")            
            times = times.timetuple()            
            times = time.mktime(times)

            abpmean.append([int(times), float(data[1])])
            hr.append([int(times), float(data[2])])
            pulse.append([int(times), float(data[3])])
            resp.append([int(times), float(data[4])])
            spo2.append([int(times), float(data[5])])
        
        with open(os.path.join(DATA_DIR, 'abpmean.json'),'r+') as abpmeanjson:
            abpmeanjson.write(str(abpmean))

        with open(os.path.join(DATA_DIR, 'hr.json'),'r+') as hrjson:
            hrjson.write(str(hr))

        with open(os.path.join(DATA_DIR, 'pulse.json'),'r+') as pulsejson:
            pulsejson.write(str(pulse))

        with open(os.path.join(DATA_DIR, 'resp.json'),'r+') as respjson:
            respjson.write(str(resp))

        with open(os.path.join(DATA_DIR, 'spo2.json'),'r+') as spo2json:
            spo2json.write(str(spo2))
        
        

        # return render(request, 'base/mahalanobis/chart.html')     

    return render(request, 'base/mahalanobis/index.html', {'data':str(abpmean), 'data_table':datay})     
            
