import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
import ROOT
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

dict = {
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

def load_data(tau3mu, file_name):
    """Load ROOT data and turn tree into a pd dataframe"""
    #print("Loading data from", file_name)
    f = uproot.open(file_name)
    tree = f["FinalTree"]
    if tau3mu == "tau3mu":
        br = branches + branches_tau3mu
    else:
        br = branches
    data = tree.arrays(br ,library="pd")
    return data

def load_dfs(dict, string):
    dfs = []
    for key, value in dict.items():
        if string in key:
            df = load_data(string, value[0])
            df['isMC'] = value[1]
            df['ID'] = key
            dfs.append(df)
    df_all = pd.concat(dfs, ignore_index=True)
    return df_all


def add_weight_nVtx(df_all):
    df_all["weight_nVtx"] = 1
    df_all["weight_nVtx_err"] = 0
    histo_file = TFile.Open("./PV_Histo/histogram_ratio.root")
    histo = {
        "B0_preE_tau3mu": None,
        "B0_postE_tau3mu": None,
        "Bp_preE_tau3mu": None,
        "Bp_postE_tau3mu": None,
        "Ds_preE_tau3mu": None,
        "Ds_postE_tau3mu": None,
        "DsPhiPi_preE_control": None,
        "DsPhiPi_postE_control": None,
    }
    for key in histo:
        name = "ratio_h_" + key.split('_')[0] + "_" + key.split('_')[1]
        histo[key] = histo_file.Get(name)

    le = len(df_all)
    with tqdm(total=le) as pbar:
        for index, row in df_all.iterrows():
            pbar.update(1)
            if row['ID'] in histo:
                bin = histo[row['ID']].FindBin(row['nVtx'])
                scale = histo[row['ID']].GetBinContent(bin)
                scale_err = histo[row['ID']].GetBinError(bin)
                df_all.at[index, "weight_nVtx"] = scale
                df_all.at[index, "weight_nVtx_err"] = scale_err

    return df_all

def add_weight_MuonSF(df_all, tau3mu=True):
    df_all["Muon1_SF"] = 1
    df_all["Muon1_SF_err"] = 0
    df_all["Muon2_SF"] = 1
    df_all["Muon2_SF_err"] = 0
    if tau3mu==True:
        df_all["Muon3_SF"] = 1
        df_all["Muon3_SF_err"] = 0
    SF_pre = TFile.Open("/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_preE.root")
    SF_post = TFile.Open("/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_postE.root")
    SFs = {
        "preE": None,
        "postE": None,
    }
    SFs["preE"] = SF_pre.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")
    SFs["postE"] = SF_post.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")
    le = len(df_all)
    with tqdm(total=le) as pbar:
        for index, row in df_all.iterrows():
            pbar.update(1)
            if "preE" in row['ID']:
                info = "preE"
            elif "postE" in row['ID']:
                info = "postE"
            else:
                info = None  
            if info is not None:
                for k in range(2+int(tau3mu)):
                    ipt = SFs[info].GetYaxis().FindBin(row["Ptmu"+str(k+1)])
                    ieta = SFs[info].GetXaxis().FindBin(abs(row["Etamu"+str(k+1)]))
                    scale = SFs[info].GetBinContent(ieta, ipt)
                    scale_err = SFs[info].GetBinError(ieta, ipt)
                    df_all.at[index, "Muon"+str(k+1)+"_SF"] = scale
                    df_all.at[index, "Muon"+str(k+1)+"_SF_err"] = scale_err

    return df_all

def add_weight_CC(df_all):
    df_all["weight_CC"] = 1
    df_all["weight_CC_err"] = 0
    le = len(df_all)
    with tqdm(total=le) as pbar:
        for index, row in df_all.iterrows():
            pbar.update(1)
            if ("preE" in row['ID']):
                df_all.at[index, "weight_CC"] = weight_CC_preE
                df_all.at[index, "weight_CC_err"] =weight_CC_preE_err
            elif ("postE" in row['ID']):
                df_all.at[index, "weight_CC"] = weight_CC_postE
                df_all.at[index, "weight_CC_err"] =weight_CC_postE_err
    return df_all

def add_weight(df_all):
    df_all["weight"] = 1
    df_all["weight_MC"] = 1
    le = len(df_all)
    weights = {
        "Ds_preE": (xsection_Ds_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Dstau/N_Ds_preE),
        "Ds_postE": (xsection_Ds_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Dstau/N_Ds_postE),
        "B0_preE": (xsection_B0_preE*lumi_tau3mu_preE*BR_tau3mu*BR_B0tau/N_B0_preE),
        "B0_postE": (xsection_B0_postE*lumi_tau3mu_postE*BR_tau3mu*BR_B0tau/N_B0_postE),
        "Bp_preE": (xsection_Bp_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Bptau/N_Bp_preE),
        "Bp_postE": (xsection_Bp_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Bptau/N_Bp_postE),
        "DsPhiPi_preE": (xsection_DsPhiPi_preE*lumi_control_preE*BR_control*BR_DsPhiPi/N_DsPhiPi_preE),
        "DsPhiPi_postE": (xsection_DsPhiPi_postE*lumi_control_postE*BR_control*BR_DsPhiPi/N_DsPhiPi_postE)
    }
    weights_MC = {
        "Ds_preE": ((N_Bp_preE/N_Ds_preE)*(BR_Dstau/BR_Bptau)),
        "Ds_postE": ((N_Bp_postE/N_Ds_postE)*(BR_Dstau/BR_Bptau)),
        "B0_preE": ((N_Bp_preE/N_B0_preE)*(BR_B0tau/BR_Bptau)),
        "B0_postE": ((N_Bp_postE/N_B0_postE)*(BR_B0tau/BR_Bptau)),
        "Bp_preE": ((N_Bp_preE/N_Bp_preE)*(BR_Bptau/BR_Bptau)),
        "Bp_postE": ((N_Bp_postE/N_Bp_postE)*(BR_Bptau/BR_Bptau))
    }
    with tqdm(total=le) as pbar:
        for index, row in df_all.iterrows():
            pbar.update(1)
            name = row['ID'].split('_')[0] + "_" + row['ID'].split('_')[1]
            if name in weights:
                df_all.at[index, "weight"] = weights[name]
            if name in weights_MC:
                df_all.at[index, "weight_MC"] = weights_MC[name]
    return df_all

def add_weight_final(df_all, full=True, tau3mu=True):
    if full==True and tau3mu==True:
        df_all['weight_final'] = df_all['weight'] * df_all['weight_MC'] * df_all['weight_CC'] * df_all['Muon3_SF'] * df_all['weight_nVtx']
    elif full==True and tau3mu==False:
        df_all['weight_final'] = df_all['weight'] * df_all['weight_nVtx']
    elif full==False and tau3mu==True:
        df_all['weight_final'] = df_all['weight'] * df_all['weight_MC']
    elif full==False and tau3mu==False:
        df_all['weight_final'] = df_all['weight']
    return df_all

if __name__ == "__main__":
    
    tau3mu=False
    full=False
    """
    if tau3mu==True:
        print("Load tau3mu files:")
        df_tau3mu = load_dfs(dict, "tau3mu")
    else:
        print("Load control files:")
        df_tau3mu = load_dfs(dict, "control")
    
    print("Done!\nAdd 'weights':")
    df_tau3mu = add_weight(df_tau3mu)
    
    if full == True:
        print("Done!\nAdd 'weight_nVtx':")
        df_tau3mu = add_weight_nVtx(df_tau3mu)

        if tau3mu==True:
            print("Done!\nAdd 'MuonSFs':")
            df_tau3mu = add_weight_MuonSF(df_tau3mu, tau3mu)
            print("Done!\nAdd 'weight_CC':")
            df_tau3mu = add_weight_CC(df_tau3mu)
    
    print("Done!\nAdd 'weight_final':")
    df_tau3mu = add_weight_final(df_tau3mu, full, tau3mu)
    print("Done!\nMake CSV file:")
    """
    if tau3mu==True:
        fileName = "ROOTFiles/AllData"
    else:
        fileName = "ROOTFiles/AllControl"
    if not os.path.exists("ROOTFiles"):
        subprocess.run(["mkdir", "ROOTFiles"])
    """
    df_tau3mu = df_tau3mu.drop('ID', axis=1)
    df_tau3mu.to_csv(fileName+".csv", index=False)
    print("File CSV saved!")
    """
    rdf = ROOT.RDF.MakeCsvDataFrame("/lustrehome/mbuonsante/Tau_3mu/CC_etc/CMSSW_13_0_13/src/"+fileName+".csv")
    cols = ROOT.vector('string')(); cols.push_back("isMC"); cols.push_back("weights");
    rdf.Snapshot("FinalTree", "pippo.root")
    print("File ROOT saved!")

    
    

