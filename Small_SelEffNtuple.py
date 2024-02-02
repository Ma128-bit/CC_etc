import sys, os, subprocess, json, time, warnings
num_cores = os.cpu_count()
print("N. CPU cores: ", num_cores)
from datetime import datetime
import numpy as np
import pandas as pd
import uproot, argparse
from multiprocessing import Pool
from file_locations import *

histonames= ["InitialPlots/hEvtCount", "PlotsAfterTrigger/hEvtCount", "PlotsAfterLooseMuon/hEvtCount", "PlotsAfter3Muons/hEvtCount", "PlotsAfterTauCand/hEvtCount"]	
b_names = [s.replace("/hEvtCount", "") for s in histonames]

def load_histo(file_name):
	"""Load ROOT data and turn tree into a pd dataframe"""
	f = uproot.open(file_name)
	sum_out = []
	list = [sum_out]
	for k in range(len(histonames)):
		obj = f[histonames[k]]
		num_entries = obj.values()
		num_entries = sum(num_entries)
		sum_out.append(num_entries)
	df = pd.DataFrame(list, columns=b_names)
	return df
        
def load_data(print_lable, input_list):
	"""Load and merge ROOT trees into a single dataset."""
	datasets = []
	j = 1
	print(" ", print_lable, "   ", 0, "/",len(input_list), end='\r')
	for entry in input_list:
		files = subprocess.check_output("find %s -type f -name '*root'" % entry, shell=True)
		for f in files.splitlines():
			datasets.append(load_histo(f.decode()))
		print(" ", print_lable, "   ", j, "/",len(input_list), "    ", end='\r')
		j=j+1
	df_all = pd.concat(datasets, ignore_index=True)
	return df_all

def make_sum(print_lable, files, csv = False):
	Run = load_data(print_lable, files)
	if csv == True:
		Run.to_csv(print_lable + ".csv", index=False)
	Run_sum = []
	for k in b_names:
		Run_sum.append(Run[k].sum())
	print("\n  Events: ", Run_sum)
	return Run_sum

if __name__ == "__main__":
    
	data_2022 = [tau3mu_files_2022C[0], tau3mu_files_2022E[2], tau3mu_files_2022F[5]]
	data_2022 = [i+"/0000" for i in data_2022]
	mc_2022 = [tau3mu_files_MC[0], tau3mu_files_MC[1]]
	mc_2022 = [i+"/0000" for i in mc_2022]
    
	data_2018 = ["/lustre/cms/store/user/fsimone/DoubleMuonLowMass/SkimTau3Mu_UL2018_Run2018D_Mini_noHLT/240131_153938/0000"]
	mc_2018 = ["/lustre/cms/store/user/fsimone/DsToTau_To3Mu_MuFilter_TuneCP5_13TeV-pythia8-evtgen/SkimTau3Mu_Summer20UL18_DsTau3Muv2_noHLT_forSynch/240131_155514/0000/"]

	with Pool() as p:
		list = p.starmap(make_sum, [('data_2022',data_2022, False),('mc_2022',mc_2022, False),('data_2018',data_2018, False),('mc_2018',mc_2018, False)])
	
	df_out = pd.DataFrame(list, columns=b_names)
	df_out['Index'] = ["data_2022", "mc_2022", "data_2018", "mc_2018"]
	column_order = ['Index'] + [col for col in df_out if col != 'Index']
	df_out = df_out[column_order]
	df_out.to_csv('EffResults/Post_Ntuple_Data_tau3mu.csv', index=False)
	print("EffResults/Post_Ntuple_tau3mu.csv Saved!")





    
