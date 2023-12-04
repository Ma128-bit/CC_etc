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

parser = argparse.ArgumentParser(description="--tau3mu and --data. Default: control and MC")
parser.add_argument("--tau3mu", action="store_true", help="Tau3mu")
parser.add_argument("--data", action="store_true", help="Enable verbose mode")
args = parser.parse_args()
is_tau3mu = args.tau3mu
data = args.data

if is_tau3mu == True:
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

        
def load_data(print_lable, input_list): #NOT USED
	"""Load and merge ROOT trees with MVA data into a single dataset."""
	datasets = []
	j = 1
	print(" ", print_lable, "   ", 0, "/",len(input_list), end='\r')
	for entry in input_list:
		files = subprocess.check_output("find %s -type f -name '*root'" % entry, shell=True)
		for f in files.splitlines():
			datasets.append(load_histo(f.decode()))
		print(" ", print_lable, "   ", j, "/",len(input_list), end='\r')
		j=j+1
	print("Done!")
	df_all = pd.concat(datasets, ignore_index=True)
	return df_all

def make_sum(print_lable, files, csv = False): #NOT USED
	Run = load_data(print_lable, files)
	if csv == True:
		Run.to_csv(print_lable + ".csv", index=False)
	Run_sum = []
	for k in histonames_CC:
		Run_sum.append(Run[k].sum())
	print(Run_sum)
	return Run_sum

if __name__ == "__main__":
	if not os.path.exists("EffResults"):
		subprocess.run(["mkdir", "EffResults"])
		
	if data == True:
		if is_tau3mu==False:
			R22C_sum = load_histo(control_Run2022C)
			R22D_sum = load_histo(control_Run2022D)
			R22E_sum = load_histo(control_Run2022E)
			R22F_sum = load_histo(control_Run2022F)
			R22G_sum = load_histo(control_Run2022G)

			list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_analysis_Data_control.csv', index=False)
		else:
			R22C_sum = load_histo(tau3mu_Run2022C)
			R22D_sum = load_histo(tau3mu_Run2022D)
			R22E_sum = load_histo(tau3mu_Run2022E)
			R22F_sum = load_histo(tau3mu_Run2022F)
			R22G_sum = load_histo(tau3mu_Run2022G)

			list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_analysis_Data_tau3mu.csv', index=False)

	else:
		if is_tau3mu==False:
			R22MC_pre_sum = load_histo(MC2022_DsPhiPi_pre)
			R22MC_post_sum = load_histo(MC2022_DsPhiPi_post)
			list = [R22MC_pre_sum, R22MC_post_sum]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["MC_2022_preE", "MC_2022_postE"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_analysis_MC_control.csv', index=False)
		else:
			MC1_p = load_histo(MC2022_Ds_pre)
			MC2_p = load_histo(MC2022_B0_pre)
			MC3_p = load_histo(MC2022_Bp_pre)
			MC1_d = load_histo(MC2022_Ds_post)
			MC2_d = load_histo(MC2022_B0_post)
			MC3_d = load_histo(MC2022_Bp_post)
			list = [MC1_p, MC2_p, MC3_p, MC1_d, MC2_d, MC3_d]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["Ds_pre", "B0_pre", "Bp_pre", "Ds_post", "B0_post", "Bp_post"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_analysis_MC_tau3mu.csv', index=False)
		
	







	
