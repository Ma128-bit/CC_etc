import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
import ROOT
import pickle
import psutil
import time
from utils import *
from tqdm import tqdm
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

Files = {
    "C_tau3mu": [tau3mu_Run2022C, 0],
    "D_tau3mu": [tau3mu_Run2022D, 0],
    "E_tau3mu": [tau3mu_Run2022E, 0],
    "F_tau3mu": [tau3mu_Run2022F, 0],
    "G_tau3mu": [tau3mu_Run2022G, 0],
    "B0_preE_tau3mu": [MC2022_B0_pre, 1],
    "B0_postE_tau3mu": [MC2022_B0_post, 1],
    "Bp_preE_tau3mu": [MC2022_Bp_pre, 2],
    "Bp_postE_tau3mu": [MC2022_Bp_post, 2],
    "Ds_preE_tau3mu": [MC2022_Ds_pre, 3],
    "Ds_postE_tau3mu": [MC2022_Ds_post, 3],
    "C_control": [control_Run2022C, 0],
    "D_control": [control_Run2022D, 0],
    "E_control": [control_Run2022E, 0],
    "F_control": [control_Run2022F, 0],
    "G_control": [control_Run2022G, 0],
    "DsPhiPi_preE_control": [MC2022_DsPhiPi_pre, 4],
    "DsPhiPi_postE_control": [MC2022_DsPhiPi_post, 4]
}
xsection_Bp_preE = 3.508e+9
xsection_Bp_postE = 3.538e+9
xsection_Ds_preE = 9.827e+9
xsection_Ds_postE = 9.815e+9
xsection_B0_preE = 3.520e+9
xsection_B0_postE = 3.525e+9
xsection_DsPhiPi_preE = 1.106e+10
xsection_DsPhiPi_postE = 1.103e+10

lumi_tau3mu_preE = 8.052
lumi_tau3mu_postE = 26.758
lumi_control_preE = 0.397
lumi_control_postE = 1.33

BR_tau3mu = 1.0e-7
BR_control = 1.29e-5

BR_Dstau = 5.48e-2
BR_DsPhiPi = 1.3e-5
BR_Bptau = 3.33e-2
BR_B0tau = 3.35e-2

N_Bp_preE = 515160
N_Bp_postE = 1627733
N_Ds_preE = 2077873
N_Ds_postE = 7428463
N_B0_preE = 837468
N_B0_postE = 2702174
N_DsPhiPi_preE = 297926
N_DsPhiPi_postE = 1199059

weight_CC_preE = 0.77
weight_CC_postE = 1.03
weight_CC_preE_err = 0.09
weight_CC_postE_err = 0.05

def load_df(treename, path):
    for key, value in Files.items():
        
        
    frame = RDataFrame(treename, path+"/*.root")
    return data
