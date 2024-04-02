import sys, os, subprocess, json
import time
start = time.time()
#import ROOT
import pickle
import argparse
from tqdm import tqdm
from ROOT import RDataFrame, gROOT, EnableImplicitMT, gInterpreter, TH1F, TString, std, TFile
#from ROOT import *
from file_locations import *

gROOT.SetBatch(True)
EnableImplicitMT()

gInterpreter.Declare("""
    #include "cpp_library.h"
""")

from ROOT import SF_WeightsComputer, PV_WeightsComputer, add_index

branches = [
    "isMC", "lumi", "run", "evt", "puFactor", "DeltaR_max", "DeltaZ_max", 
    "Pmu3", "cLP", "tKink", "segmComp", "tripletMass", "fv_nC", "fv_dphi3D", 
    "fv_d3D", "fv_d3Dsig", "d0", "d0sig", "d0sig_max", "mindca_iso", "trkRel", 
    "Ptmu1", "Etamu1", "Ptmu2", "Etamu2", "Ptmu3", "Etamu3", "Pmu1", "Pmu2", 
    "P_tripl", "Pt_tripl", "Eta_tripl", "MVA1", "MVA2", "MVASoft1", "MVASoft2", 
    "ChargeMu1", "ChargeMu2", "ChargeMu3", "nVtx", 
    "L1_DoubleMu0_er1p5", "L1_DoubleMu0_er1p4","L1_DoubleMu4_dR1p2","L1_DoubleMu4p5_dR1p2",
    "L1_DoubleMu0_er2p0","L1_DoubleMu0_er2p0_bk"
]

branches_tau3mu =[
    "tripletMassReso", "category", "MVA3", "MVASoft3", "dimu_OS1", "dimu_OS2", 
    "nTracks03_mu1", "nTracks03_mu2", "nTracks03_mu3", "nTracks05_mu1", "nTracks05_mu2", "nTracks05_mu3",
    "sumPt03_mu1", "sumPt03_mu2", "sumPt03_mu3", "sumPt05_mu1", "sumPt05_mu2", "sumPt05_mu3",
    "L1_TripleMu_5SQ_3SQ_0","L1_TripleMu_5SQ_3SQ_0OQ",
    "L1_TripleMu_3SQ_2p5SQ_0OQ_Mass_Max12","L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max12"
]

branches_MVA =[
    "Vx", "Vy", "Vz", "cQ_uS_", "cQ_tK_", "cQ_gK_", "cQ_tRChi2_",
    "cQ_sRChi2_", "cQ_Chi2LP_", "cQ_Chi2LM_", "cQ_lD_", "cQ_gDEP_", "cQ_tM_", "cQ_gTP_", 
    "match1_dX_", "match1_pullX_", "match1_pullDxDz_", "match1_dY_", "match1_pullY_", "match1_pullDyDz_", 
    "match2_dX_", "match2_pullX_", "match2_pullDxDz_", "match2_dY_", "match2_pullY_", "match2_pullDyDz_", 
    "validMuonHitComb", "nValidTrackerHits",
    "nValidPixelHits", "GL_nValidMuHits", "nStationsMu", "nMatchesMu", 
    "innerTrk_ValidFraction_", "innerTrk_highPurity_", 
    "innerTrk_normChi2_", "outerTrk_normChi2_" "outerTrk_muStValidHits_"   
]

branches_tau3mu = branches_tau3mu + [var + "1" for var in branches_MVA] + [var + "2" for var in branches_MVA] + [var + "3" for var in branches_MVA]

Files = {
    "tau3mu2022": [tau3mu_Run2022C, tau3mu_Run2022D, tau3mu_Run2022E, tau3mu_Run2022F, tau3mu_Run2022G, MC2022_B0_pre, MC2022_B0_post, MC2022_Bp_pre, MC2022_Bp_post, MC2022_Ds_pre, MC2022_Ds_post],
    "tau3mu2023": [tau3mu_Run2023B, tau3mu_Run2023C, tau3mu_Run2023D],
    "control2022": [control_Run2022C, control_Run2022D, control_Run2022E, control_Run2022F, control_Run2022G, MC2022_DsPhiPi_pre, MC2022_DsPhiPi_post],
    "control2023": []
}

def load_df(isTau3mu, year, treename):
    if isTau3mu == True:
        files = Files["tau3mu"+str(year)]
        br = branches+branches_tau3mu
    else:
        files = Files["control"+str(year)]
        br = branches
    frame = RDataFrame(treename, files, br)
    return frame

def check_type():
    parser = argparse.ArgumentParser(description="Set tau3mu or control")
    parser.add_argument("--type", type=str, help="tau3mu or control")
    args = parser.parse_args()
    type = args.type
    if "tau3mu" in type:
        return True, int(type.replace("tau3mu", ""))
    elif "control" in type:
        return False, int(type.replace("control", ""))
    else:
        print("ERROR: choose --type between tau3mu and control")
        sys.exit()
        

if __name__ == "__main__":
    isTau3mu, year = check_type()
    
    print("Starting!")
    start_2 = time.time()
    df = load_df(isTau3mu, year,  "FinalTree")
    df = df.Define("year", add_index(year))
    df = df.DefinePerSample("ID", "add_ID(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight", "add_weight(rdfslot_, rdfsampleinfo_)")
    if isTau3mu==True:
        df = df.DefinePerSample("weight_MC", "add_weight_MC(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight_CC", "add_weight_CC(rdfslot_, rdfsampleinfo_)")
    df = df.DefinePerSample("weight_CC_err", "add_weight_CC_err(rdfslot_, rdfsampleinfo_)")

    SF_f1 = TFile.Open(single_mu_SF_preE)
    SF_f2 = TFile.Open(single_mu_SF_postE)
    SF_pre = SF_f1.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")
    SF_post = SF_f2.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")

    df = df.Define("Muon1_SF", SF_WeightsComputer(SF_pre, SF_post, False), ["ID", "Ptmu1", "Etamu1"])
    df = df.Define("Muon2_SF", SF_WeightsComputer(SF_pre, SF_post, False), ["ID", "Ptmu2", "Etamu2"])
    df = df.Define("Muon1_SF_err", SF_WeightsComputer(SF_pre, SF_post, True), ["ID", "Ptmu1", "Etamu1"])
    df = df.Define("Muon2_SF_err", SF_WeightsComputer(SF_pre, SF_post, True), ["ID", "Ptmu2", "Etamu2"])
    if isTau3mu==True:
        df = df.Define("Muon3_SF", SF_WeightsComputer(SF_pre, SF_post, False), ["ID", "Ptmu3", "Etamu3"])
        df = df.Define("Muon3_SF_err", SF_WeightsComputer(SF_pre, SF_post, True), ["ID", "Ptmu3", "Etamu3"])

    histo_file = TFile.Open(PV_SFs)
    h_vectors = std.vector(TH1F)()
    h_name = std.vector(TString)()
    h_names = ["B0_preE", "B0_postE", "Bp_preE", "Bp_postE", "Ds_preE", "Ds_postE", "DsPhiPi_preE", "DsPhiPi_postE"]
    for key in h_names:
        h_vectors.push_back(histo_file.Get("ratio_h_" + key))
        h_name.push_back(key)
    
    df = df.Define("weight_nVtx", PV_WeightsComputer(h_name, h_vectors, False), ["ID", "nVtx"])
    df = df.Define("weight_nVtx_err", PV_WeightsComputer(h_name, h_vectors, True), ["ID", "nVtx"])    

    if not os.path.exists("ROOTFiles"):
        subprocess.run(["mkdir", "ROOTFiles"])

    df = df.Define("vtx_prob","add_vrtx_proba(fv_nC)")
    branches.append("vtx_prob")
    
    if isTau3mu==True:
        #Filters for omega and phi:
        df = df.Filter("(abs(dimu_OS1-0.782)>0.033 && category==0) || (abs(dimu_OS1-0.782)>0.048 && category==1) || (abs(dimu_OS1-0.782)>0.066 && category==2)")
        df = df.Filter("(abs(dimu_OS2-0.782)>0.033 && category==0) || (abs(dimu_OS2-0.782)>0.048 && category==1) || (abs(dimu_OS2-0.782)>0.066 && category==2)")
        df = df.Filter("(abs(dimu_OS1-1.019)>0.033 && category==0) || (abs(dimu_OS1-1.019)>0.045 && category==1) || (abs(dimu_OS1-1.019)>0.056 && category==2)")
        df = df.Filter("(abs(dimu_OS2-1.019)>0.033 && category==0) || (abs(dimu_OS2-1.019)>0.045 && category==1) || (abs(dimu_OS2-1.019)>0.056 && category==2)")
        
        b_weights = ["ID", "year", "weight", "weight_MC", "weight_CC", "weight_CC_err", "Muon3_SF","Muon2_SF","Muon1_SF","Muon3_SF_err","Muon2_SF_err","Muon1_SF_err","weight_nVtx", "weight_nVtx_err", "training_weight", "combine_weight"]
        df = df.Define("training_weight", "weight_MC * weight_CC * Muon3_SF * weight_nVtx")
        df = df.Define("combine_weight", "weight * weight_CC * Muon3_SF * weight_nVtx")
        df.Snapshot("FinalTree", "ROOTFiles/AllData"+str(year)+".root", branches+branches_tau3mu+b_weights)
    else:
        b_weights = ["ID", "year", "weight","Muon1_SF","Muon2_SF","Muon1_SF_err","Muon2_SF_err","weight_nVtx", "weight_nVtx_err", "control_weight"]
        df = df.Define("control_weight", "weight * weight_nVtx")
        df.Snapshot("FinalTree", "ROOTFiles/AllControl"+str(year)+".root", branches+b_weights)
    
    print("Performed ",df.GetNRuns()," loops")
    end = time.time()
    print('Partial execution time ', end-start_2)
    print('Total execution time ', end-start)



