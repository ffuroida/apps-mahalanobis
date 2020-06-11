import weka.core.jvm as jvm
from weka.core.converters import Loader
jvm.start() 
from weka.classifiers import Evaluation
from weka.classifiers import Random
from weka.core.dataset import Stats
load = Loader(classname="weka.core.converters.ArffLoader")
anomali = load.load_file('dataset1.arff')
anomali.no_class()

data_test = [] #menampung n-sliding
n = input('window size : ')
rec = n

size = anomali.num_instances 
#menghapus tanggal
anomali.delete_attribute(1) 
#backup atribut class
backup_class = anomali.values(anomali.num_attributes-1) 
#setelah di backup maka dihapus
anomali.delete_attribute(anomali.num_attributes-1) 
#hapus index 
anomali.delete_first_attribute()
n = int(n)
for x in range(n):
    y = str(anomali.get_instance(x)).split(',')
    data_test.append(y)
    anomali.delete(0) #menghapus index sliding window

# inisiasi list untuk data tes
names = []
# inisiasi values tiap - tiap atribut
data_inst = [] 
# inisiasi untuk memasykkan hasil prediksi dari setiap datates
data_pred = [] 
# penampung masing2 STD
data_std = []
anomali_out = [] 
anomali_per_baris = []
# bisa cek data yang digunakan
# anomali

n_attr = anomali.num_attributes
row = anomali.num_instances
n_inst = (anomali.num_instances) * n_attr
# output
# data_test[0]

for x in range(n_attr):
    names.append(anomali.attribute(x))

    anomali.class_is_first()

def proses():  #diluar def index = 0
    import math
    from weka.classifiers import Kernel, KernelClassifier
    from weka.classifiers import PredictionOutput
    import numpy as np
    klasifi = KernelClassifier(classname="weka.classifiers.functions.SMOreg", options=["-N","0"])
    vm = Kernel(classname="weka.classifiers.functions.supportVector.RBFKernel", options=["-G","0.1"])
    klasifi.vm = vm
    output_x = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText")
    kelola = Evaluation(anomali)
    kelola.crossvalidate_model(klasifi,anomali, 10, Random(0), output=output_x)
    process = 0
    for x in anomali.values(anomali.class_index):
        data_inst.append(x)
    for x in kelola.predictions:
        i = str(x)
        index = i.split()
        data_pred.append(float(index[2]))
    data_std.insert(idx,math.ceil(np.std(data_inst))*0.1)
    print ('\n DONE PROCESSING DATASET ATTRIBUTE ', anomali.attribute(anomali.class_index),'...')
def inisiasi_anomali():
    print (len(data_pred))
    baris = 0
    start = 0
    for ite in range(n_attr):
        for inisiasi in range(row):
            if ite == 0:
                err = abs(data_pred[inisiasi]-data_inst[inisiasi])
                if err > data_std[ite]:
                    anomali_out.append(1)
                else:
                    anomali_out.append(0)
                baris = inisiasi
                start = baris
            else:
                err = abs(data_pred[baris]-data_inst[baris])
                if err > data_std[ite]:
                    anomali_out.append(1)
                else:
                    anomali_out.append(0)
                baris += 1
        start = baris
        baris = start
def view():
    start = 0
    an = []
    data_anomali = []
    record = int(rec)
    #record = rec
    for n in range(row):
        if n == 0:
            print ('\nTransformatting.....')
            print ('Record ke - ', record,' ', data_inst[0],', ',data_inst[row*1],', ',data_inst[row*2],', ',data_inst[row*3],', ',data_inst[row*4])
            print ('PREDICT : ', data_pred[0],', ',data_pred[row*1],', ',data_pred[row*2],', ',data_pred[row*3],', ',data_pred[row*4])
            print ('STD     : ', data_std[0:4])
            count_an = 0
            count_not = 0
            data_anomali = []
            for y in range(n_attr):
                if anomali_out[start] == 1:
                    data_anomali.append(names[y])
                    count_an += 1
                    start += 1
                else:
                    count_not += 1
                    start += 1
            print ('An anomali : ', data_anomali)
            if count_an > count_not:
                anomali_per_baris.append(1)
                an.append(record)
            else:
                anomali_per_baris.append(0)
            print ('\n-------PEMISAH---------\n')
        else:
            print ('\nTransformatting.....')
            print ('Record ke - ', record+1,' ', data_inst[0+n],', ',data_inst[(row*1)+n],', ',data_inst[(row*2)+n],', ',data_inst[(row*3)+n],', ',data_inst[(row*4)+n])
            print ('PREDICT : ', data_pred[0+n],', ',data_pred[(row*1)+n],', ',data_pred[(row*2)+n],', ',data_pred[(row*3)+n],', ',data_pred[(row*4)+n])
            print ('STD     : ', data_std[0:4])
            data_anomali = []
            count_an = 0 
            count_not = 0
            for y in range(n_attr):
                if anomali_out[start] == 1:
                    data_anomali.append(names[y])
                    count_an += 1
                    start += 1
                else:
                    count_not += 1
                    start += 1
            print ('An anomali : ', data_anomali)
            if count_an > count_not:
                anomali_per_baris.append(1)
                an.append(record)
            else:
                anomali_per_baris.append(0)
            print ('\n-------PEMISAH---------\n')
            record += 1
    for x in range(len(an)):
        print ('Record of ',an[x],' is an anomaly')
    print ('Count : ', len(an))
for idx in range(n_attr):
    proses()
    anomali.no_class()
    anomali.delete_first_attribute()
    if idx == 4:
        break
    else:
        anomali.class_is_first()
inisiasi_anomali()
view()

import math
predict_true = 0
predict_false = 0
predict = []
data_train = []
start = 0
val = 0
for x in range(n_attr):
    for y in range(row):
        if x == 0:
            klasifikasi = math.ceil((abs(data_inst[y]-data_pred[y])/data_inst[y])*100)
            err = math.ceil(abs(data_inst[y]-data_pred[y]))
            if klasifikasi == err:
                predict_true += 1
            else:
                predict_false += 1
            if predict_true > predict_false:
                predict.append(1)
            else:
                predict.append(0)
            start = y
        else:
            klasifikasi = math.ceil((abs(data_inst[start]-data_pred[start])/data_inst[start])*100)
            err = math.ceil(abs(data_inst[y]-data_pred[y]))
            if klasifikasi == err:
                predict_true += 1
            else:
                predict_false += 1
            if predict_true > predict_false:
                predict.append(1)
            else:
                predict.append(0)
start = 0
error = 0
print (len(anomali_per_baris), ' ' , len(predict))
for x in range(row):
    cout = (str(int(data_inst[0+x]))+' '+str(int(data_inst[(row*1)+x]))+' '+ str(int(data_inst[(row*2)+x]))+' '+ str(int(data_inst[(row*3)+x]))+' '+ str(int(data_inst[(row*4)+x]))).split()
    data_train.append(cout)
for x in range(row):
    counting = 0
    for y in data_test[start]:
        if y in data_train[x]:
            counting += 1
    if counting >= 3:
        val = anomali_per_baris[x]
        anomali_per_baris.insert(start, val)
    else:
        anomali_per_baris.insert(start, 1)
    start += 1
    if start == n:
        break
print (len(anomali_per_baris), ' ' , len(predict))

import math
start = 0
TP = 0
FN = 0
FP = 0
TN = 0
n = 0
for x in range(size):
    if(backup_class[x] == 0) and (anomali_per_baris[x] == 0):
        TP += 1
    elif(backup_class[x] == 0) and (anomali_per_baris[x] == 1) and (predict[x] == 0):
        FN += 1
    elif(backup_class[x] == 1) and (anomali_per_baris[x] == 0) and (predict[x] == 1):
        FP += 1
    elif predict[x] == 1:
        TN += 1 #Anomali sesungguhnya
DR = (float(TP)/(float(TP+FN)))* 100
FPR = (float(FP)/(float(FP+TN)))* 100
print ('True Positive  : ',TP)
print ('False Positive : ',FP)
print ('False Negative : ',FN)
print ('True Negative  : ',TN,'\n')
print ('Detection Rate : ',DR)
print ('False Positive Rate : ', FPR)