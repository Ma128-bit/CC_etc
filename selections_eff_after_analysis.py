import sys, os, subprocess, json
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
import numpy as np
warnings.filterwarnings("default", category=UserWarning, module="numpy")
import pandas as pd
import uproot

histoname= "CutEff_NEvents"
cut_names = ["BeforeCuts","L1_fired","HLT_fired","MuonID","DiMu_mass","TriMu_mass","mu1_TrMatch","mu12_TrMatch","mu123_TrMatch"]

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
	data_path = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/Analysis/JobAdd_perEra/"

	files_2022C = [
		"Era_C_control.root"
	]

	files_2022D = [
		"Era_D_control.root"
	]

	files_2022E = [
		"Era_E_control.root"
	]

	files_2022F = [
		"Era_F_control.root"
	]

	files_2022G = [
		"Era_G_control.root"
	]
	
	files_Run2022C = [data_path + i for i in files_2022C]
	files_Run2022D = [data_path + i for i in files_2022D]
	files_Run2022E = [data_path + i for i in files_2022E]
	files_Run2022F = [data_path + i for i in files_2022F]
	files_Run2022G = [data_path + i for i in files_2022G]

	R22C_sum = load_histo(files_Run2022C[0])
	R22D_sum = load_histo(files_Run2022D[0])
	R22E_sum = load_histo(files_Run2022E[0])
	R22F_sum = load_histo(files_Run2022F[0])
	R22G_sum = load_histo(files_Run2022G[0])

	list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
	df_out = pd.DataFrame(list, columns=cut_names)
	df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
	df_out.to_csv('Post_analysis.csv', index=False)
	







	
