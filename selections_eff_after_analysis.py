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

is_tau3mu= True
data = False

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
	data_path = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/Analysis/"

	files_2022C = [
		"JobAdd_perEra/Era_C_control.root"
	]

	files_2022D = [
		"JobAdd_perEra/Era_D_control.root"
	]

	files_2022E = [
		"JobAdd_perEra/Era_E_control.root"
	]

	files_2022F = [
		"JobAdd_perEra/Era_F_control.root"
	]

	files_2022G = [
		"JobAdd_perEra/Era_G_control.root"
	]

	files_2022_MC_pre = [
		"DsPhiPi_preE_tau3mu_ReReco/AnalysedTree_MC_DsPhiPi_preE_tau3mu_merged_ReReco.root",
		"Ds_preE_tau3mu_ReReco/AnalysedTree_MC_Ds_preE_tau3mu_merged_ReReco.root",
		"B0_preE_tau3mu_ReReco/AnalysedTree_MC_B0_preE_tau3mu_merged_ReReco.root",
		"Bp_preE_tau3mu_ReReco/AnalysedTree_MC_Bp_preE_tau3mu_merged_ReReco.root"
	]

	files_2022_MC_post = [
		"DsPhiPi_postE_tau3mu_ReReco/AnalysedTree_MC_DsPhiPi_postE_tau3mu_merged_ReReco.root",
		"Ds_postE_tau3mu_ReReco/AnalysedTree_MC_Ds_postE_tau3mu_merged_ReReco.root",
		"B0_postE_tau3mu_ReReco/AnalysedTree_MC_B0_postE_tau3mu_merged_ReReco.root",
		"Bp_postE_tau3mu_ReReco/AnalysedTree_MC_Bp_postE_tau3mu_merged_ReReco.root"
	]
	
	files_Run2022C = [data_path + i for i in files_2022C]
	files_Run2022D = [data_path + i for i in files_2022D]
	files_Run2022E = [data_path + i for i in files_2022E]
	files_Run2022F = [data_path + i for i in files_2022F]
	files_Run2022G = [data_path + i for i in files_2022G]

	files_Run2022_MC_pre = [data_path + i for i in files_2022_MC_pre]
	files_Run2022_MC_post = [data_path + i for i in files_2022_MC_post]

	if data == True:
		R22C_sum = load_histo(files_Run2022C[0])
		R22D_sum = load_histo(files_Run2022D[0])
		R22E_sum = load_histo(files_Run2022E[0])
		R22F_sum = load_histo(files_Run2022F[0])
		R22G_sum = load_histo(files_Run2022G[0])

		list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
		df_out = pd.DataFrame(list, columns=cut_names)
		df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
		column_order = ['Index'] + [col for col in df_out if col != 'Index']
		df_out = df_out[column_order]
		df_out.to_csv('Post_analysis_Data.csv', index=False)
	else:
		if is_tau3mu==False:
			R22MC_pre_sum = load_histo(files_Run2022_MC_pre[0])
			R22MC_post_sum = load_histo(files_Run2022_MC_post[0])
			list = [R22MC_pre_sum, R22MC_post_sum]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["MC_2022_preE", "MC_2022_postE"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('Post_analysis_MC_control.csv', index=False)
		else:
			MC1_p = load_histo(files_Run2022_MC_pre[1])
			MC2_p = load_histo(files_Run2022_MC_pre[2])
			MC3_p = load_histo(files_Run2022_MC_pre[3])
			MC1_d = load_histo(files_Run2022_MC_post[1])
			MC2_d = load_histo(files_Run2022_MC_post[2])
			MC3_d = load_histo(files_Run2022_MC_post[3])
			list = [MC1_p, MC2_p, MC3_p, MC1_d, MC2_d, MC3_d]
			df_out = pd.DataFrame(list, columns=cut_names)
			df_out['Index'] = ["Ds_pre", "B0_pre", "Bp_pre", "Ds_post", "B0_post", "Bp_post"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('Post_analysis_MC_tau3mu.csv', index=False)
		
	







	
