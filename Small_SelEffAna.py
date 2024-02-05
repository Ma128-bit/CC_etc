import sys, os, subprocess, json
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
import numpy as np
warnings.filterwarnings("default", category=UserWarning, module="numpy")
import pandas as pd
import uproot
import argparse
from file_locations import *

histoname= "CutEff_NEvents"
cut_names = ["BeforeCuts","L1_fired","HLT_fired","MuonID","DiMu_mass","TriMu_mass","mu1_TrMatch","mu12_TrMatch","mu123_TrMatch"]
cut_names[4]="BS-SV_sign_deltaR-Z"

def load_histo(file_name):
	"""Load ROOT data and turn tree into a pd dataframe"""
	f = uproot.open(file_name)
	obj = f[histoname]
	num_entries = obj.values()
	return num_entries


def load_data(file_list):
    """Load and merge ROOT trees with MVA data into a single dataset."""
    num_entries = None  
    for entry in file_list:
        num = load_histo(entry)
        if num_entries is None:
            num_entries = num  
        else:
            num_entries = [a + b for a, b in zip(num_entries, num)]  
    print("Done!")
    return num_entries



if __name__ == "__main__":
	if not os.path.exists("EffResults"):
		subprocess.run(["mkdir", "EffResults"])

	data22 = ["/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022C_0_tau3mu_PromptReco/AnalysedTree_data_2022C_0_tau3mu0.root", 
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022C_0_tau3mu_PromptReco/AnalysedTree_data_2022C_0_tau3mu1.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022C_0_tau3mu_PromptReco/AnalysedTree_data_2022C_0_tau3mu2.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022C_0_tau3mu_PromptReco/AnalysedTree_data_2022C_0_tau3mu3.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022E_2_tau3mu_PromptReco/AnalysedTree_data_2022E_2_tau3mu0.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022E_2_tau3mu_PromptReco/AnalysedTree_data_2022E_2_tau3mu1.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022E_2_tau3mu_PromptReco/AnalysedTree_data_2022E_2_tau3mu2.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu0.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu1.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu2.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu3.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu4.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu5.root",
		  "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/2022F_5_tau3mu_PromptReco/AnalysedTree_data_2022F_5_tau3mu6.root"]
	
	MC22 = ["/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/MC_Ds_postE.root",
		"/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/MC_Ds_preE.root"]
	
	data18 = ["/lustrehome/mbuonsante/Tau_3mu/Ntuple/2018Ntuple/CMSSW_13_0_13/src/Analysis/2018D_tau3mu_Test2018_HLT/AnalysedTree_data_2018D_tau3mu"+str(j)+".root" for j in range(7)]
	
	MC18 = ["/lustrehome/mbuonsante/Tau_3mu/Ntuple/2018Ntuple/CMSSW_13_0_13/src/Analysis/Ds_2018_tau3mu_Test2018_HLT/AnalysedTree_MC_Ds_2018_tau3mu0.root"]

	R22_sum = load_data(data22)
	MC22_sum = load_data(MC22)

	R18_sum = load_data(data18)
	MC18_sum = load_data(MC18)

	list = [R22_sum, MC22_sum, R18_sum, MC18_sum]
	df_out = pd.DataFrame(list, columns=cut_names)
	df_out['Index'] = ["R22_sum", "MC22_sum", "R18_sum", "MC18_sum"]
	column_order = ['Index'] + [col for col in df_out if col != 'Index']
	df_out = df_out[column_order]
	df_out.to_csv('EffResults/Post_analysis_Data_tau3mu.csv', index=False)

		
	







	
