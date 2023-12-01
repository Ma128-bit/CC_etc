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
from multiprocessing import Pool

tname= ["TreeMakerBkg/ntuple", "TreeMakerBkg/ntuple", "Tree3Mu/ntuple", "Tree3Mu/ntuple"]

def fit_era(dataset, era):
    if (dataset=='MC'):
        nome="TreeMakerBkg/ntuple"
    if (dataset=='MC_CC'):
        nome="Tree3Mu/ntuple"
    t1 = TChain(nome)
    MCprocess = era
    path=''
    if dataset == 'MC' and MCprocess == 'Ds_preE':
        path = '/lustre/cms/store/user/mbuonsan/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_preE/230504_170059'
    if dataset == 'MC' and MCprocess == 'Ds_postE':
        path = '/lustre/cms/store/user/mbuonsan/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_postE/230504_170127'
    if dataset == 'MC' and MCprocess == 'Bp_preE':
        path = '/lustre/cms/store/user/mbuonsan/ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_preE/230504_170043'
    if dataset == 'MC' and MCprocess == 'Bp_postE':
        path = '/lustre/cms/store/user/mbuonsan/ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_postE/230504_170114'
    if dataset == 'MC' and MCprocess == 'B0_preE':
        path = '/lustre/cms/store/user/mbuonsan/BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_preE/230504_170029'
    if dataset == 'MC' and MCprocess == 'B0_postE':
        path = '/lustre/cms/store/user/mbuonsan/BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_postE/230504_170014'
    if dataset == 'MC_CC' and MCprocess == 'DsPhiMuNu':
        path = '/lustre/cms/store/user/caruta/Pythia8_DsPhiMuNu_Run3_2022/SkimTau3mu_MCRun3_DsPhiMuNu_Mini_v4/230114_172745'
    if dataset == 'MC_CC' and MCprocess == 'DsPhiPi_preE':
        path = '/lustre/cms/store/user/mbuonsan/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_preE/230507_103411'
    if dataset == 'MC_CC' and MCprocess == 'DsPhiPi_postE':
        path = '/lustre/cms/store/user/mbuonsan/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_postE/230507_103348'
        
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
    file = TFile.Open('histogram_nVTx_MC.root', 'UPDATE')
    h.Write()
    file.Close()

if __name__=='__main__':
    f = TFile("histogram_nVTx_MC.root", "RECREATE")
    f.Close()
    fit_era('MC','Ds_preE')
    fit_era('MC','Ds_postE')
    fit_era('MC','Bp_preE')
    fit_era('MC','Bp_postE')
    fit_era('MC','B0_preE')
    fit_era('MC','B0_postE')
    fit_era('MC_CC','DsPhiPi_preE')
    fit_era('MC_CC','DsPhiPi_postE')
'''
if __name__=='__main__':
    dat = ['data', 'dataE', 'data_control', 'data_controlE']
    #dat = ['data']
    er=['C', 'D', 'E', 'F', 'G']
    indx = ['_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7']
    h = []
    cont = 0
    
    for dataset in dat:
        t1 = TChain(tname[cont])
        for era in er:
            for ind in indx:
                run = '2022'+era+ind
                if dataset == 'data' and run == '2022C_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_stream0_Mini_v3/230504_135403'
                if dataset == 'data' and run == '2022C_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_stream1_Mini_v3/230504_135433'
                if dataset == 'data' and run == '2022C_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_stream2_Mini_v3/230504_135502'
                if dataset == 'data' and run == '2022C_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_stream3_Mini_v3/230504_135532'
                if dataset == 'data' and run == '2022C_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_stream4_Mini_v3/230504_135604'
                if dataset == 'data' and run == '2022C_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_stream5_Mini_v3/230504_135636'
                if dataset == 'data' and run == '2022C_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_stream6_Mini_v3/230504_135709'
                if dataset == 'data' and run == '2022C_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_stream7_Mini_v3/230504_135740'
                  
                if dataset == 'data' and run == '2022D_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD_stream0_Mini_v3/230504_151331'
                if dataset == 'data' and run == '2022D_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD_stream1_Mini_v3/230504_151401'
                if dataset == 'data' and run == '2022D_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD_stream2_Mini_v3/230504_151432'
                if dataset == 'data' and run == '2022D_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD_stream3_Mini_v3/230504_151502'
                if dataset == 'data' and run == '2022D_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD_stream4_Mini_v3/230504_151531'
                if dataset == 'data' and run == '2022D_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD_stream5_Mini_v3/230504_151602'
                if dataset == 'data' and run == '2022D_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD_stream6_Mini_v3/230504_151632'
                if dataset == 'data' and run == '2022D_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD_stream7_Mini_v3/230504_151704'
                
                if dataset == 'dataE' and run == '2022E_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraE_stream0_Mini_v3/230504_151737'
                if dataset == 'dataE' and run == '2022E_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraE_stream1_Mini_v3/230504_151808'
                if dataset == 'dataE' and run == '2022E_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraE_stream2_Mini_v3/230504_151840'
                if dataset == 'dataE' and run == '2022E_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraE_stream3_Mini_v3/230504_151911'
                if dataset == 'dataE' and run == '2022E_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraE_stream4_Mini_v3/230504_151942'
                if dataset == 'dataE' and run == '2022E_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraE_stream5_Mini_v3/230504_152013'
                if dataset == 'dataE' and run == '2022E_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraE_stream6_Mini_v3/230504_152044'
                if dataset == 'dataE' and run == '2022E_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraE_stream7_Mini_v3/230504_152114'
                  
                if dataset == 'dataE' and run == '2022F_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraF_stream0_Mini_v3/230504_152143'
                if dataset == 'dataE' and run == '2022F_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraF_stream1_Mini_v3/230504_152215'
                if dataset == 'dataE' and run == '2022F_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraF_stream2_Mini_v3/230504_152245'
                if dataset == 'dataE' and run == '2022F_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraF_stream3_Mini_v3/230504_152316'
                if dataset == 'dataE' and run == '2022F_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraF_stream4_Mini_v3/230504_152345'
                if dataset == 'dataE' and run == '2022F_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraF_stream5_Mini_v3/230504_152415'
                if dataset == 'dataE' and run == '2022F_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraF_stream6_Mini_v3/230504_152445'
                if dataset == 'dataE' and run == '2022F_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraF_stream7_Mini_v3/230504_152514'
                  
                if dataset == 'dataE' and run == '2022G_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraG_stream0_Mini_v3/230504_152632'
                if dataset == 'dataE' and run == '2022G_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraG_stream1_Mini_v3/230504_152651'
                if dataset == 'dataE' and run == '2022G_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraG_stream2_Mini_v3/230504_152711'
                if dataset == 'dataE' and run == '2022G_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraG_stream3_Mini_v3/230504_152731'
                if dataset == 'dataE' and run == '2022G_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraG_stream4_Mini_v3/230504_152751'
                if dataset == 'dataE' and run == '2022G_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraG_stream5_Mini_v3/230504_152812'
                if dataset == 'dataE' and run == '2022G_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraG_stream6_Mini_v3/230504_152833'
                if dataset == 'dataE' and run == '2022G_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraG_stream7_Mini_v3/230504_152853'

                if dataset == 'data_control' and run == '2022C_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraC_stream0_Mini_v3/230507_105546'
                if dataset == 'data_control' and run == '2022C_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraC_stream1_Mini_v3/230507_105617'
                if dataset == 'data_control' and run == '2022C_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraC_stream2_Mini_v3/230507_105648'
                if dataset == 'data_control' and run == '2022C_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraC_stream3_Mini_v3/230507_105718'
                if dataset == 'data_control' and run == '2022C_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraC_stream4_Mini_v3/230507_105748'
                if dataset == 'data_control' and run == '2022C_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraC_stream5_Mini_v3/230507_105817'
                if dataset == 'data_control' and run == '2022C_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraC_stream6_Mini_v3/230507_105847'
                if dataset == 'data_control' and run == '2022C_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraC_stream7_Mini_v3/230507_105917'
                  
                if dataset == 'data_control' and run == '2022D_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD_stream0_Mini_v3/230507_105929'
                if dataset == 'data_control' and run == '2022D_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD_stream1_Mini_v3/230507_105959'
                if dataset == 'data_control' and run == '2022D_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD_stream2_Mini_v3/230507_110030'
                if dataset == 'data_control' and run == '2022D_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD_stream3_Mini_v3/230507_110101'
                if dataset == 'data_control' and run == '2022D_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD_stream4_Mini_v3/230507_110135'
                if dataset == 'data_control' and run == '2022D_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD_stream5_Mini_v3/230507_110209'
                if dataset == 'data_control' and run == '2022D_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD_stream6_Mini_v3/230507_110239'
                if dataset == 'data_control' and run == '2022D_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD_stream7_Mini_v3/230507_110308'
                
                if dataset == 'data_controlE' and run == '2022E_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraE_stream0_Mini_v3/230507_110320'
                if dataset == 'data_controlE' and run == '2022E_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraE_stream1_Mini_v3/230507_110348'
                if dataset == 'data_controlE' and run == '2022E_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraE_stream2_Mini_v3/230507_110418'
                if dataset == 'data_controlE' and run == '2022E_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraE_stream3_Mini_v3/230507_110448'
                if dataset == 'data_controlE' and run == '2022E_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraE_stream4_Mini_v3/230507_110518'
                if dataset == 'data_controlE' and run == '2022E_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraE_stream5_Mini_v3/230507_110549'
                if dataset == 'data_controlE' and run == '2022E_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraE_stream6_Mini_v3/230507_110619'
                if dataset == 'data_controlE' and run == '2022E_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraE_stream7_Mini_v3/230507_110649'
                  
                if dataset == 'data_controlE' and run == '2022F_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraF_stream0_Mini_v3/230507_110700'
                if dataset == 'data_controlE' and run == '2022F_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraF_stream1_Mini_v3/230507_110734'
                if dataset == 'data_controlE' and run == '2022F_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraF_stream2_Mini_v3/230507_110806'
                if dataset == 'data_controlE' and run == '2022F_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraF_stream3_Mini_v3/230507_110838'
                if dataset == 'data_controlE' and run == '2022F_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraF_stream4_Mini_v3/230507_110908'
                if dataset == 'data_controlE' and run == '2022F_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraF_stream5_Mini_v3/230507_110939'
                if dataset == 'data_controlE' and run == '2022F_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraF_stream6_Mini_v3/230507_111009'
                if dataset == 'data_controlE' and run == '2022F_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraF_stream7_Mini_v3/230507_111039'
                  
                if dataset == 'data_controlE' and run == '2022G_0':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraG_stream0_Mini_v3/230507_111050'
                if dataset == 'data_controlE' and run == '2022G_1':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraG_stream1_Mini_v3/230507_111120'
                if dataset == 'data_controlE' and run == '2022G_2':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraG_stream2_Mini_v3/230507_111149'
                if dataset == 'data_controlE' and run == '2022G_3':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraG_stream3_Mini_v3/230507_111218'
                if dataset == 'data_controlE' and run == '2022G_4':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraG_stream4_Mini_v3/230507_111248'
                if dataset == 'data_controlE' and run == '2022G_5':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraG_stream5_Mini_v3/230507_111319'
                if dataset == 'data_controlE' and run == '2022G_6':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraG_stream6_Mini_v3/230507_111352'
                if dataset == 'data_controlE' and run == '2022G_7':
                    path = '/lustre/cms/store/user/mbuonsan/ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraG_stream7_Mini_v3/230507_111424'
                
                for r, d, f in os.walk(path):
                    for file in f:
                        if '.root' in file:
                            print(os.path.join(r, file))
                            t1.Add(os.path.join(r, file))
        title="h"+"["+ str(cont) + "]"
        title1="h"+"["+ str(cont) + "] "+ dat[cont]
        h.append(TH1F(title,title1,80,0,80))
        print("Plot:")
        t1.Draw("PVCollection_Size>>h["+str(cont)+"]","","N")
        cont = cont +1
    f = TFile("histogram_nVTx.root", "RECREATE")
    for l in range(len(h)):
        print("Salvo file")
        h[l].Write()
    f.Close()
    
    if dataset == 'MC' and MCprocess == 'Ds_preE':
        path = '/lustre/cms/store/user/mbuonsan/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_preE/230504_170059'
    if dataset == 'MC' and MCprocess == 'Ds_postE':
        path = '/lustre/cms/store/user/mbuonsan/DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_postE/230504_170127'
    if dataset == 'MC' and MCprocess == 'Bp_preE':
        path = '/lustre/cms/store/user/mbuonsan/ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_preE/230504_170043'
    if dataset == 'MC' and MCprocess == 'Bp_postE':
        path = '/lustre/cms/store/user/mbuonsan/ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_postE/230504_170114'
    if dataset == 'MC' and MCprocess == 'B0_preE':
        path = '/lustre/cms/store/user/mbuonsan/BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_preE/230504_170029'
    if dataset == 'MC' and MCprocess == 'B0_postE':
        path = '/lustre/cms/store/user/mbuonsan/BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_postE/230504_170014'
    if dataset == 'MC' and MCprocess == 'DsPhiMuNu':
        path = '/lustre/cms/store/user/caruta/Pythia8_DsPhiMuNu_Run3_2022/SkimTau3mu_MCRun3_DsPhiMuNu_Mini_v4/230114_172745'
    if dataset == 'MC' and MCprocess == 'DsPhiPi_preE':
        path = '/lustre/cms/store/user/mbuonsan/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_preE/230507_103411'
    if dataset == 'MC' and MCprocess == 'DsPhiPi_postE':
        path = '/lustre/cms/store/user/mbuonsan/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_postE/230507_103348'
    '''
    
