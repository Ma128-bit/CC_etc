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

ROOT.gROOT.SetBatch(True)

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
    "tau3mu": [tau3mu_Run2022C, tau3mu_Run2022D, tau3mu_Run2022E, tau3mu_Run2022F, tau3mu_Run2022G, MC2022_B0_pre, MC2022_B0_post, MC2022_Bp_pre, MC2022_Bp_post, MC2022_Ds_pre, MC2022_Ds_post],
    "control": [control_Run2022C, control_Run2022D, control_Run2022E, control_Run2022F, control_Run2022G, MC2022_DsPhiPi_pre, MC2022_DsPhiPi_post]
}

def load_df(isTau3mu, treename):
    if isTau3mu == True:
        files = Files["tau3mu"]
        br = branches+branches_tau3mu
    else:
        files = Files["control"]
        br = branches
    frame = RDataFrame(treename, files, br)
    return frame

ROOT.gInterpreter.Declare("""
    #include "cpp_library.h"
""")

if __name__ == "__main__":
    df = load_df(True, "FinalTree")
    entries = df.Count()
    print("total ",entries.GetValue())
    df = df.DefinePerSample("weight", "add_weight(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight_MC", "add_weight_MC(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight_CC", "add_weight_CC(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight_CC_err", "add_weight_CC_err(rdfslot_, rdfsampleinfo_)")
    weight = df.Histo1D(("weight", "weight", 1000, 0, 0.001), "weight");
    canvas = ROOT.TCanvas("c", "c", 800, 800)
    canvas.cd()
    weight.Draw("Hist")
    canvas.SaveAs("prova.png")
    print("performed ",df.GetNRuns()," loops")



