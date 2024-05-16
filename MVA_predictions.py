import sys, os, subprocess, uproot, joblib
import numpy as np
import pandas as pd
from ROOT import RDF
from sklearn.ensemble import HistGradientBoostingClassifier

branches_MVA =[
    "Ptmu", "Etamu", 
    "Vx", "Vy", "Vz", 
    "cQ_uS_", "cQ_tK_", "cQ_gK_", "cQ_tRChi2_",
    "cQ_sRChi2_", "cQ_Chi2LP_", "cQ_Chi2LM_", "cQ_lD_", "cQ_gDEP_", "cQ_tM_", "cQ_gTP_", 
    "match1_dX_", "match1_pullX_", "match1_pullDxDz_", "match1_dY_", "match1_pullY_", "match1_pullDyDz_", 
    "match2_dX_", "match2_pullX_", "match2_pullDxDz_", "match2_dY_", "match2_pullY_", "match2_pullDyDz_", 
    "validMuonHitComb", "nValidTrackerHits",
    "nValidPixelHits", "GL_nValidMuHits", "nStMu", "nMatchesMu", 
    "innerTrk_ValidFraction_", "innerTrk_highPurity_", 
    "innerTrk_normChi2_", "outerTrk_normChi2_", "outerTrk_muStValidHits_"   
]
"""
branches_MVA = [
    'cQ_Chi2LP_',
    'cQ_tK_',
    'nValidTrackerHits',
    'nValidPixelHits',
    'innerTrk_ValidFraction_',
    'cQ_Chi2LM_',
    'cQ_sRChi2_',
    'cQ_tRChi2_',
    'cQ_gDEP_',
    'cQ_gK_',
    'trkLayersWMeas',
    'nStMu',
    'segmComp_',
    'GLnormChi2_mu',
    'innerTrk_normChi2_',
    'outerTrk_normChi2_'
]
"""
def load_data(file_names):
    """Load ROOT data and turn tree into a pd dataframe"""
    trees = []
    for file in file_names:
        print("Loading data from", file)
        f = uproot.open(file)
        tree = f["FinalTree"]
        trees.append(tree.arrays(library="pd"))
    trees[1]["Vx1"] = trees[1]["Vx1"] - trees[1]["Vx1"].mean() + trees[0]["Vx1"].mean()
    trees[1]["Vy1"] = trees[1]["Vy1"] - trees[1]["Vy1"].mean() + trees[0]["Vy1"].mean()
    trees[1]["Vz1"] = trees[1]["Vz1"] - trees[1]["Vz1"].mean() + trees[0]["Vz1"].mean()
    data = pd.concat(trees)
    return data

def save_data(data, fileName):
    data.to_csv(fileName+".csv", index=False)
    print("File CSV saved!")
    del data
    rdf = RDF.FromCSV(fileName+".csv")
    rdf.Snapshot("FinalTree", fileName+".root")
    print("File ROOT saved!")

def predict(data, index, model):
    print("Start prediction label: ", index)
    branches = [var + str(index) for var in branches_MVA]
    X = data[branches]
    X = X.values
    predictionsID = model.predict(X)
    predictions = model.predict_proba(X)
    data["privateMVAID_mu"+str(index)] = predictionsID
    data["privateMVA_mu"+str(index)] = predictions[:,1]
    del predictions
    del predictionsID
    del X
    #print("Done!")
    return data


if __name__ == "__main__":
    files = ["/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/Era_F_tau3mu.root",
             "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/MC_Ds_preE.root"]
    model = joblib.load('Tau3MuMVA_PtEtaReweight_VShift.pkl')
    #model = joblib.load('Tau3MuMVA_PtEtaReweight_NoVxVyVz.pkl')
    #model = joblib.load('privateMVA.pkl')
    data = load_data(files)
    """
    branches_temp = [var + str(1) for var in branches_MVA] + [var + str(2) for var in branches_MVA] + [var + str(3) for var in branches_MVA]
    for v in branches_temp:
        print(v, " : ", (data[v] == -99).sum())
    
    print(len(data))
    data = data[(data[branches_temp] != -99).all(axis=1)]
    """
    #for i in range(1,4):
    for i in range(1,3):
        data = predict(data, i, model)
    save_data(data, "Run3")

