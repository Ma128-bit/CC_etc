import sys, os, subprocess       
import math
import string
import os.path
import array
import glob
import random
import array as ary
import numpy as np
import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
from file_locations import *
from multiprocessing import Pool
num_cores = os.cpu_count()
print("N. CPU cores: ", num_cores)
if num_cores/4<3:
	print("WARNING: 12 CPU cores are recommended to run code at full speed")
    
def fit_era(dataset, era):
    if (dataset=='data' or dataset=='MC'):
        nome="TreeMakerBkg/ntuple"
    if (dataset=='data_control' or dataset=='MC_CC'):
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

    if dataset=='data' or dataset=='data_control':
        histo_name = "PV_Histo/histogram_nVTx.root"
        for i in range(len(paths)):
            path = paths[i]
            if path!='':
                for r, d, f in os.walk(path):
                    for file in f:
                        if '.root' in file:
                            #print(os.path.join(r, file))
                            t1.Add(os.path.join(r, file))

    if dataset == 'MC':
        if era == 'Ds_preE':
            path = tau3mu_files_MC[0]
        elif era == 'Ds_postE':
            path = tau3mu_files_MC[1]
        elif era == 'Bp_preE':
            path = tau3mu_files_MC[2]
        elif era == 'Bp_postE':
            path = tau3mu_files_MC[3]
        elif era == 'B0_preE':
            path = tau3mu_files_MC[4]
        elif era == 'B0_postE':
            path = tau3mu_files_MC[5]
        else:
            path = ''

    if dataset == 'MC_CC':
        if era == 'DsPhiPi_preE':
            path = control_files_MC[0]
        elif era == 'DsPhiPi_postE':
            path = control_files_MC[1]
        else:
            path = ''
	
    if (dataset == 'MC' or dataset == 'MC_CC') and path!='':
        histo_name = "PV_Histo/histogram_nVTx_MC.root"
        for r, d, f in os.walk(path):
            for file in f:
                if '.root' in file:
                    #print(os.path.join(r, file))
                    t1.Add(os.path.join(r, file))


    title="h_"+dataset+"_"+era
    title1="h_"+dataset+"_"+era
    h = TH1F(title,title1,80,0,80)
    #h.append(TH1F(title,title1,80,0,80))
    t1.Draw("PVCollection_Size>>"+title,"","N")

	
    file = None
    j = 0
    while file is None:
        file = TFile.Open(histo_name, 'UPDATE')
        if j>0:
            print(dataset, " ", era, "in while ...")
        j= j +1
    h.Write()
    file.Close()
    print(dataset, " ", era, " Done")

if __name__=='__main__':
    if not os.path.exists("PV_Histo"):
        subprocess.run(["mkdir", "PV_Histo"])
    f = TFile("PV_Histo/histogram_nVTx.root", "RECREATE")
    f.Close()
    f2 = TFile("PV_Histo/histogram_nVTx_MC.root", "RECREATE")
    f2.Close()
    print("Start with the MCs ...")
    fit_era('MC','Ds_preE')
    fit_era('MC','Ds_postE')
    fit_era('MC','Bp_preE')
    fit_era('MC','Bp_postE')
    fit_era('MC','B0_preE')
    fit_era('MC','B0_postE')
    fit_era('MC_CC','DsPhiPi_preE')
    fit_era('MC_CC','DsPhiPi_postE')
    print("Done!\nNow run on data in parallel, it will take a bit 'of time ...")
    with Pool() as p:
        p.starmap(fit_era, [('data','C'), ('data','D'), ('data','E'), ('data','F1'), ('data','F2'), ('data','G'), ('data_control','C'), ('data_control','D'), ('data_control','E'), ('data_control','F1'), ('data_control','F2'), ('data_control','G')])
        #p.starmap(fit_era, [('MC_CC','DsPhiPi_preE')])
    print("Done!\nNow getting the ratio...")
    subprocess.run("root -l PV_ratio_hist.C", shell=True)
