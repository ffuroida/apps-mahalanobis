from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from anomalydetection.forms.views import MahalanobisCreateForm
import json, csv, re, time, os
from datetime import datetime
from anomalydetection.settings import DATA_DIR, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage

from anomalydetection.mahalanobis import main, smoreg
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
    thresh = []
    data_anomaly = []
    anomaly = []
    mob_dist = []    
    data_test_value = 0
    final_data = []
    data_smoreg = []
    data_tn = 0
    data_fp = 0
    data_fn = 0
    data_tp = 0
    fpr = 0
    DetectRate = 0
    rmse = 0
    data_tabel = None

    if request.method == 'POST' and request.FILES['docfile']:        
        fs = FileSystemStorage()        
        myfile = request.FILES['docfile']
        data_test_value = request.POST['data_test_value']
        data_test_value = float("0."+str(data_test_value))

        try:
            os.remove(os.path.join(MEDIA_ROOT, myfile.name))
        except:
            pass

        filename = fs.save(myfile.name, myfile)
        if request.POST['metode'] == 'distance':
            final_data = main(myfile.name, 0.2)                       
            data_fn = final_data['fn']
            data_tn = final_data['tn']
            data_fp = final_data['fp']
            data_tp =  final_data['tp']
            DetectRate = final_data['DetectRate']
            fpr =  final_data['fpr']
            rmse = final_data['rmse']
            data_tabel = final_data['anomaly'].to_html(classes= 'table table-responsive table-bordered table-stripped')

            for index, data in zip(final_data['anomaly'].Timeseries, final_data['anomaly'].Anomaly):
                anomaly.append([index, 1 if data is True else 0])   
                data_anomaly.append({"index":index,"anomaly":data})                           
        
            for index, data in zip(final_data['anomaly'].Timeseries, final_data['anomaly'].Thresh):
                thresh.append([index, data])
                
            for index, data in zip(final_data['anomaly'].Timeseries, final_data['anomaly'].Mob_dist):
                mob_dist.append([index, data])                        
                # print(loop, data)
                
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
                        
            
            with open(os.path.join(DATA_DIR, 'mob_dist.json'),'r+') as mob_distjson:
                mob_distjson.write(str(mob_dist))
                
            with open(os.path.join(DATA_DIR, 'thresh.json'),'r+') as threshjson:
                threshjson.write(str(thresh))
            
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
                
            with open(os.path.join(DATA_DIR, 'anomaly.json'),'r+') as anomalyjson:
                anomalyjson.write(str(anomaly))

            # return render(request, 'base/mahalanobis/chart.html') 
        else:
            datay = smoreg(myfile.name)  
            xa = {'time': list(datay.time), 'abpmean': list(datay.ABPmean), 'pulse': list(datay.PULSE), 'hr': list(datay.HR), 'resp': list(datay.RESP), 'spo2': list(datay.SpO2), 'class': list(datay['class'])}            
            print(datay['time'])
            data_smoreg = datay.to_html(classes= 'table table-responsive table-bordered table-stripped')
        return render(request, 'base/mahalanobis/index.html', {'data':str(abpmean), 
                                                                'data_table':datay,
                                                                'data_percentage_test': data_test_value,
                                                                'data_anomaly': data_anomaly,
                                                                'data_tn': data_tn,
                                                                'data_fp': data_fp,
                                                                'data_fn': data_fn,
                                                                'data_tp': data_tp,
                                                                'DetectRate' : DetectRate,
                                                                'fpr' : fpr,
                                                                'rmse' : rmse,
                                                                'data_smoreg': data_smoreg,
                                                                'data_final': data_tabel})
                                                                # 'data_final': final_data})    

        # return render(request, 'base/mahalanobis/chart.html')
             

    else:
        open(os.path.join(DATA_DIR, 'mob_dist.json'),'w').close()
        open(os.path.join(DATA_DIR, 'thresh.json'),'w').close()
        open(os.path.join(DATA_DIR, 'abpmean.json'),'w').close()
        open(os.path.join(DATA_DIR, 'hr.json'),'w').close()
        open(os.path.join(DATA_DIR, 'pulse.json'),'w').close()
        open(os.path.join(DATA_DIR, 'resp.json'),'w').close()
        open(os.path.join(DATA_DIR, 'spo2.json'),'w').close()
        open(os.path.join(DATA_DIR, 'anomaly.json'),'w').close()

        
        return render(request, 'base/mahalanobis/index.html')
            

