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

ROOT.gInterpreter.Declare(
"""
int add_weight(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    double xsection_Bp_preE = 3.508e+9, xsection_Bp_postE = 3.538e+9;
    double xsection_Ds_preE = 9.827e+9, xsection_Ds_postE = 9.815e+9;
    double xsection_B0_preE = 3.520e+9, xsection_B0_postE = 3.525e+9;
    double xsection_DsPhiPi_preE = 1.106e+10, xsection_DsPhiPi_postE = 1.103e+10;

    double lumi_tau3mu_preE = 8.052, lumi_tau3mu_postE = 26.758;
    double lumi_control_preE = 0.397, lumi_control_postE = 1.33;

    double BR_tau3mu = 1.0e-7, BR_control = 1.29e-5;

    double BR_Dstau = 5.48e-2, BR_DsPhiPi = 1.3e-5;
    double BR_Bptau = 3.33e-2, BR_B0tau = 3.35e-2;

    int N_Bp_preE = 515160, N_Bp_postE = 1627733;
    int N_Ds_preE = 2077873, N_Ds_postE = 7428463;
    int N_B0_preE = 837468, N_B0_postE = 2702174;
    int N_DsPhiPi_preE = 297926, N_DsPhiPi_postE = 1199059;

    std::cout<<"id: "<<id.AsString()<<std::endl;
    std::cout<<(xsection_Ds_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Dstau/N_Ds_preE)<<std::endl;
    if(id.Contains("MC_Ds_preE.root")) return (xsection_Ds_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Dstau/N_Ds_preE);
    else if(id.Contains("MC_Ds_postE.root")) return (xsection_Ds_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Dstau/N_Ds_postE);
    else if(id.Contains("MC_B0_preE.root")) return (xsection_B0_preE*lumi_tau3mu_preE*BR_tau3mu*BR_B0tau/N_B0_preE);
    else if(id.Contains("MC_B0_postE.root")) return (xsection_B0_postE*lumi_tau3mu_postE*BR_tau3mu*BR_B0tau/N_B0_postE);
    else if(id.Contains("MC_Bp_preE.root")) return (xsection_Bp_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Bptau/N_Bp_preE);
    else if(id.Contains("MC_Bp_postE.root")) return (xsection_Bp_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Bptau/N_Bp_postE);
    else if(id.Contains("MC_DsPhiPi_preE.root")) return (xsection_DsPhiPi_preE*lumi_control_preE*BR_control*BR_DsPhiPi/N_DsPhiPi_preE);
    else if(id.Contains("MC_DsPhiPi_postE.root")) return (xsection_DsPhiPi_postE*lumi_control_postE*BR_control*BR_DsPhiPi/N_DsPhiPi_postE);
    else return 1;
}
""")

if __name__ == "__main__":
    df = load_df(True, "FinalTree")
    df = df.DefinePerSample("weight", "add_weight(rdfslot_, rdfsampleinfo_)")
    weight = df.Histo1D(("weight", "weight", 1000, 0, 0.000001), "weight");
    canvas = ROOT.TCanvas("c", "c", 800, 800)
    canvas.cd()
    weight.Draw("Hist")
    canvas.SaveAs("prova.png")


