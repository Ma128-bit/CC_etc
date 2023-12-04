import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
import matplotlib.pyplot as plt
from ROOT import *
from file_locations import *

branches = [
    "isMC", "lumi", "run", "evt", "puFactor", "DeltaR_max", "DeltaZ_max", 
    "Pmu3", "cLP", "tKink", "segmComp", "tripletMass", "fv_nC", "fv_dphi3D", 
    "fv_d3D", "fv_d3Dsig", "d0", "d0sig", "d0sig_max", "mindca_iso", "trkRel", 
    "Ptmu1", "Etamu1", "Ptmu2", "Etamu2", "Ptmu3", "Etamu3", "Pmu1", "Pmu2", 
    "P_tripl", "Pt_tripl", "Eta_tripl", "MVA1", "MVA2", "MVASoft1", "MVASoft2", 
    "ChargeMu1", "ChargeMu2", "ChargeMu3", "nVtx"
]
branches_tau3mu =[
    "tripletMassReso", "category", "MVA3", "MVASoft3", "dimu_OS1", "dimu_OS2"
]

dict = {
    "C_tau3mu": [True, tau3mu_Run2022C, 0],
    "D_tau3mu": [True, tau3mu_Run2022D, 0],
    "E_tau3mu": [True, tau3mu_Run2022E, 0],
    "F_tau3mu": [True, tau3mu_Run2022F, 0],
    "G_tau3mu": [True, tau3mu_Run2022G, 0],
    "B0_preE_tau3mu": [True, MC2022_B0_pre, 1],
    "B0_postE_tau3mu": [True, MC2022_B0_post, 1],
    "Bp_preE_tau3mu": [True, MC2022_Bp_pre, 2],
    "Bp_postE_tau3mu": [True, MC2022_Bp_post, 2],
    "Ds_preE_tau3mu": [True, MC2022_Ds_pre, 3],
    "Ds_post_tau3mu": [True, MC2022_Ds_post, 3],
    "C_control": [True, control_Run2022C, 0],
    "D_control": [True, control_Run2022D, 0],
    "E_control": [True, control_Run2022E, 0],
    "F_control": [True, control_Run2022F, 0],
    "G_control": [True, control_Run2022G, 0],
    "DsPhiPi_preE_control": [True, MC2022_DsPhiPi_pre, 4],
    "DsPhiPi_postE_control": [True, MC2022_DsPhiPi_post, 4],
}

def load_data(tau3mu, file_name):
    """Load ROOT data and turn tree into a pd dataframe"""
    print("Loading data from", file_name)
    f = uproot.open(file_name)
    tree = f["FinalTree"]
    if tau3mu == True:
        br = branches + branches_tau3mu
    else:
        br = branches
    data = tree.arrays(br ,library="pd")
    return data

def load_dfs(dict, string):
    dfs = []
    for key, value in dict.items():
        if string in key:
            df = load_data(value[0], value[1])
            df['isMC'] = value[2]
            df['ID'] = key
            dfs.append(df)
    df_all = pd.concat(dfs, ignore_index=True)
    return df_all

def add_weight_nVtx(df_all):
    nVtx = df_all['nVtx'].values
    ID = df_all['ID'].values
    weight_nVtx = np.ones(len(ID))
    histo_file = TFile.Open("./PV_Histo/histogram_ratio.root")
    histo = {
        "B0_pre_tau3mu": None,
        "B0_post_tau3mu": None,
        "Bp_pre_tau3mu": None,
        "Bp_post_tau3mu": None,
        "Ds_pre_tau3mu": None,
        "DsPhiPi_pre_control": None,
        "DsPhiPi_post_control": None,
    }
    for key in histo:
        name = key.split('_')[0] + key.split('_')[1]
        histo[key] = histo_file.Get("ratio_h_"+ name)
    for i in range(len(ID)):
        if ID[i] in histo:
            weight_nVtx[i] = histo[ID[i]].GetBinContent(histo[ID[i]].FindBin(nVtx[i]))
    df_all = df_all.assign("weight_nVtx"=weight_nVtx)
    return df_all

if __name__ == "__main__":
    df_tau3mu = load_dfs(dict, "tau3mu")
    print(df_tau3mu)
    df_tau3mu = add_weight_nVtx(df_tau3mu)
    print(df_tau3mu)
    print(df_tau3mu["weight_nVtx"])
    
    

