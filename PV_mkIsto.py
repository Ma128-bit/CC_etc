import os        
import sys       
import math
import string
import os.path
import array
import glob
import random
import array as ary
import numpy as np
from ROOT import *
from file_locations import *
from multiprocessing import Pool
num_cores = os.cpu_count()
print("N. CPU cores: ", num_cores)
if num_cores/4<3:
	print("WARNING: 12 CPU cores are recommended to run code at full speed")
    
def fit_era(dataset, era):
    indx = ['_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7']
    if (dataset=='data' or dataset=='dataE' or dataset=='dataE2'):
        nome="TreeMakerBkg/ntuple"
    if (dataset=='data_control' or dataset=='data_controlE'):
        nome="Tree3Mu/ntuple"
    t1 = TChain(nome)
    if dataset == 'data':
        if era == 'C':
            paths = tau3mu_files_2022C
        elif era == 'D':
            paths = tau3mu_files_2022D1 + tau3mu_files_2022D2
        elif era == 'E':
            paths = tau3mu_files_2022E
        elif era == 'F1':
            paths = tau3mu_files_2022F[:4]
        elif era == 'F2':
            paths = tau3mu_files_2022F[-4:]
        elif era == 'G':
            paths = tau3mu_files_2022G
        else:
            paths = []
            
    if dataset == 'data_control':
        if era == 'C':
            paths = control_files_2022C
        elif era == 'D':
            paths = control_files_2022D1 + control_files_2022D2
        elif era == 'E':
            paths = control_files_2022E
        elif era == 'F1':
            paths = control_files_2022F[:4]
        elif era == 'F2':
            paths = control_files_2022F[-4:]
        elif era == 'G':
            paths = control_files_2022G
        else:
            paths = []

    for i in range(len(paths)):
        path = paths[i]
        if path!='':
            for r, d, f in os.walk(path):
                for file in f:
                    if '.root' in file:
                        print(os.path.join(r, file))
                        t1.Add(os.path.join(r, file))

    title="h_"+dataset+"_"+era
    title1="h_"+dataset+"_"+era
    h = TH1F(title,title1,80,0,80)
    #h.append(TH1F(title,title1,80,0,80))
    t1.Draw("PVCollection_Size>>"+title,"","N")
    
    file = None
    while file is None:
        file = TFile.Open('histogram_nVTx.root', 'UPDATE')
    h.Write()
    file.Close()

if __name__=='__main__':
    f = TFile("histogram_nVTx.root", "RECREATE")
    f.Close()
    with Pool() as p:
        p.starmap(fit_era, [('data','C'), ('data','D'), ('data','E'), ('data','F1'), ('data','F2'), ('data','G'), ('data_control','C'), ('data_control','D'), ('data_control','E'), ('data_control','F2'), ('data_control','F2'), ('data_control','G')])
