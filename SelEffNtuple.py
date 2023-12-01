import sys, os, subprocess, json
num_cores = os.cpu_count()
print("N. CPU cores: ", num_cores)
import warnings
import time
from datetime import datetime
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
import numpy as np
warnings.filterwarnings("default", category=UserWarning, module="numpy")
import pandas as pd
import uproot
import argparse
from multiprocessing import Pool
from file_locations import *

histonames_CC= ["InitialPlots/hEvtCount", "PlotsAfterTrigger/hEvtCount", "PlotsAfterOnePFCand/hEvtCount", "PlotsAfterLooseMuon/hEvtCount", "PlotsAfterDiMuonCand/hEvtCount", "PlotsAfter2Mu1Track/hEvtCount", "PlotsAfterPhiPiCandSel/hEvtCount"]

parser = argparse.ArgumentParser(description="--tau3mu and --data. Default: control and MC")
parser.add_argument("--tau3mu", action="store_true", help="Tau3mu")
parser.add_argument("--data", action="store_true", help="Enable verbose mode")
args = parser.parse_args()
is_Tau3mu = args.tau3mu
data = args.data

if num_cores/4<2 and data==True:
	print("WARNING: 8 CPU cores are recommended to run code at full speed")
	
if is_Tau3mu == True:
	histonames_CC= ["InitialPlots/hEvtCount", "PlotsAfterTrigger/hEvtCount", "PlotsAfterLooseMuon/hEvtCount", "PlotsAfter3Muons/hEvtCount", "PlotsAfterTauCand/hEvtCount"]

C_names = [s.replace("/hEvtCount", "") for s in histonames_CC]
def load_histo(file_name):
	"""Load ROOT data and turn tree into a pd dataframe"""
	#print("Loading data from", file_name)
	f = uproot.open(file_name)
	sum_out = []
	list = [sum_out]
	for k in range(len(histonames_CC)):
		obj = f[histonames_CC[k]]
		num_entries = obj.values()
		num_entries = sum(num_entries)
		sum_out.append(num_entries)
	df = pd.DataFrame(list, columns=C_names)
	return df

        
def load_data(print_lable, input_list):
	"""Load and merge ROOT trees with MVA data into a single dataset."""
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
	for k in C_names:
		Run_sum.append(Run[k].sum())
	print("\n  Events: ", Run_sum)
	return Run_sum

if __name__ == "__main__":
	
	CCfiles_Run2022C = [i+"/0000" for i in control_files_2022C]
	CCfiles_Run2022D1 = [i+"/0000" for i in control_files_2022D1]
	CCfiles_Run2022D2 = [i+"/0000" for i in control_files_2022D2]
	CCfiles_Run2022D = CCfiles_Run2022D1 + CCfiles_Run2022D2
	CCfiles_Run2022E = [i+"/0000" for i in control_files_2022E]
	CCfiles_Run2022F = [i+"/0000" for i in control_files_2022F]
	CCfiles_Run2022F_part1 = CCfiles_Run2022F[::2] 
	CCfiles_Run2022F_part2 = CCfiles_Run2022F[1::2]
	CCfiles_Run2022G = [i+"/0000" for i in control_files_2022G]

	Taufiles_Run2022C = [i+"/0000" for i in tau3mu_files_2022C]
	Taufiles_Run2022D1 = [i+"/0000" for i in tau3mu_files_2022D1]
	Taufiles_Run2022D2 = [i+"/0000" for i in tau3mu_files_2022D1]
	Taufiles_Run2022D = Taufiles_Run2022D1 + Taufiles_Run2022D2
	Taufiles_Run2022E = [i+"/0000" for i in tau3mu_files_2022E]
	Taufiles_Run2022F = [i+"/0000" for i in tau3mu_files_2022F]
	Taufiles_Run2022F_part1 = Taufiles_Run2022F[::2] 
	Taufiles_Run2022F_part2 = Taufiles_Run2022F[1::2]
	Taufiles_Run2022G = [i+"/0000" for i in tau3mu_files_2022G]

	files_Run2022_MC_tau3mu_pre = [i+"/0000" for i in tau3mu_files_MC if "preE" in i]
	files_Run2022_MC_tau3mu_post = [i+"/0000" for i in tau3mu_files_MC if "postE" in i]

	files_Run2022_MC_control_pre = [i+"/0000" for i in control_files_MC if "preE" in i]
	files_Run2022_MC_control_post = [i+"/0000" for i in control_files_MC if "postE" in i]

	if not os.path.exists("EffResults"):
		subprocess.run(["mkdir", "EffResults"])
	start_time = time.time()
	if data == True:
		if is_Tau3mu == False:
			with Pool() as p:
        			list = p.starmap(make_sum, [('Run_22C',CCfiles_Run2022C, False),('Run_22D',CCfiles_Run2022D, False),('Run_22E',CCfiles_Run2022E, False),('Run_22F_1',CCfiles_Run2022F_part1, False), ('Run_22F_2',CCfiles_Run2022F_part2, False),('Run_22G',CCfiles_Run2022G, False)])
			'''
			R22C_sum = make_sum("Run_22C", CCfiles_Run2022C, csv = False)
			R22D_sum = make_sum("Run_22D", CCfiles_Run2022D, csv = False)
			R22E_sum = make_sum("Run_22E", CCfiles_Run2022E, csv = False)
			R22F_sum = make_sum("Run_22F", CCfiles_Run2022F, csv = False)
			R22G_sum = make_sum("Run_22G", CCfiles_Run2022G, csv = False)
			#R23C_v4_sum = make_sum("Run_23C_v4", files_Run2023C_v4, csv = False)

			list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
   			'''
			df_out = pd.DataFrame(list, columns=C_names)
			df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F_1", "Run_22F_2", "Run_22G"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_Ntuple_Data_Control.csv', index=False)
			print("EffResults/Post_Ntuple_Data_Control.csv Saved!")
		else:
			with Pool() as p:
        			list = p.starmap(make_sum, [('Run_22C',Taufiles_Run2022C, False),('Run_22D',Taufiles_Run2022D, False),('Run_22E',Taufiles_Run2022E, False),('Run_22F_1',Taufiles_Run2022F_part1, False), ('Run_22F_2',Taufiles_Run2022F_part2, False),('Run_22G',Taufiles_Run2022G, False)])

			df_out = pd.DataFrame(list, columns=C_names)
			df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F_1", "Run_22F_2", "Run_22G"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_Ntuple_Data_tau3mu.csv', index=False)
			print("EffResults/Post_Ntuple_Data_tau3mu.csv Saved!")

	else:
		if is_Tau3mu == False:
			Run_2022_MC_pre = make_sum("MC_2022_pre", files_Run2022_MC_control_pre, csv = False)
			Run_2022_MC_post = make_sum("MC_2022_post", files_Run2022_MC_control_post, csv = False)
			list = [Run_2022_MC_pre, Run_2022_MC_post]
			df_out = pd.DataFrame(list, columns=C_names)
			df_out['Index'] = ["MC_2022_pre", "MC_2022_post"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_Ntuple_MC_Control.csv', index=False)
			print("EffResults/Post_Ntuple_MC_Control.csv Saved!")
		else:
			Run_2022_MC_pre = make_sum("MC_2022_pre", files_Run2022_MC_tau3mu_pre, csv = False)
			Run_2022_MC_post = make_sum("MC_2022_post", files_Run2022_MC_tau3mu_post, csv = False)
			list = [Run_2022_MC_pre, Run_2022_MC_post]
			df_out = pd.DataFrame(list, columns=C_names)
			df_out['Index'] = ["MC_2022_pre", "MC_2022_post"]
			column_order = ['Index'] + [col for col in df_out if col != 'Index']
			df_out = df_out[column_order]
			df_out.to_csv('EffResults/Post_Ntuple_MC_tau3mu.csv', index=False)
			print("EffResults/Post_Ntuple_MC_tau3mu.csv Saved!")
	
	end_time = time.time()
	execution_time = (end_time - start_time)/60
	formatted_time = "{:.{}f}".format(execution_time, 2)
	print(f"Execution time: {formatted_time} min")







	
