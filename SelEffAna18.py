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
	#print("Loading data from", file_name)
	f = uproot.open(file_name)
	obj = f[histoname]
	num_entries = obj.values()
	#list = [num_entries]
	#df = pd.DataFrame(list, columns=cut_names)
	return num_entries

  
if __name__ == "__main__":
	if not os.path.exists("EffResults"):
		subprocess.run(["mkdir", "EffResults"])
		
	R22C_sum = load_histo(tau3mu_Run2022C)
	R22D_sum = load_histo(tau3mu_Run2022D)
	R22E_sum = load_histo(tau3mu_Run2022E)
	R22F_sum = load_histo(tau3mu_Run2022F)
	R22G_sum = load_histo(tau3mu_Run2022G)
	MC1_p = load_histo(MC2022_Ds_pre)
	MC2_p = load_histo(MC2022_B0_pre)
	MC3_p = load_histo(MC2022_Bp_pre)
	MC1_d = load_histo(MC2022_Ds_post)
	MC2_d = load_histo(MC2022_B0_post)
	MC3_d = load_histo(MC2022_Bp_post)

  /lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis

	list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
	df_out = pd.DataFrame(list, columns=cut_names)
	df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
	column_order = ['Index'] + [col for col in df_out if col != 'Index']
	df_out = df_out[column_order]
	df_out.to_csv('EffResults/Post_analysis_Data_tau3mu.csv', index=False)

		
	







	
