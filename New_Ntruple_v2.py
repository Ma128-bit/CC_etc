import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
import ROOT
import pickle
import psutil
import time
from tqdm import tqdm
from ROOT import RDataFrame
from ROOT import *
from file_locations import *
from values import *

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

def load_df(isTau3mu, treename):
    if isTau3mu == True:
        string = "tau3mu"
    else:
        string = "control"
    files = []
    for key, value in Files.items():
        if string in key:
            files.append(value[0])
    frame = RDataFrame(treename, files)
    return frame

ROOT.gInterpreter.Declare(
"""
float MCLable(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    std::cout<<"id: "<<id<<std::endl;
    if(id.Contains("Era_")) return 0;
    else if(id.Contains("MC_B0")) return 1;
    else if(id.Contains("MC_Bp")) return 2;
    else if(id.Contains("MC_Ds_")) return 3;
    else if(id.Contains("MC_DsPhiPi")) return 4;
    else return -1;
}
""")

if __name__ == "__main__":
    df = load_df(True, "FinalTree")
    #df.DefinePerSample("isMC", "MCLable(rdfslot_, rdfsampleinfo_)")
    is_MC = df.Histo1D(("isMC", "isMC", 7, 0, 6), "isMC");
    canvas = ROOT.TCanvas("c", "c", 800, 800)
    canvas.cd()
    is_MC.Draw("Hist")
    canvas.SaveAs("prova.png")


