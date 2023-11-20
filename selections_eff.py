import sys, os, subprocess, json
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
import numpy as np
warnings.filterwarnings("default", category=UserWarning, module="numpy")
import pandas as pd
import uproot

histonames_CC= ["InitialPlots/hEvtCount", "PlotsAfterTrigger/hEvtCount", "PlotsAfterOnePFCand/hEvtCount", "PlotsAfterLooseMuon/hEvtCount", "PlotsAfterDiMuonCand/hEvtCount", "PlotsAfter2Mu1Track/hEvtCount", "PlotsAfterPhiPiCandSel/hEvtCount"]
C_names = [s.replace("/hEvtCount", "") for s in histonames_CC]
data = False

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
		print(" ", print_lable, "   ", j, "/",len(input_list), end='\r')
		j=j+1
	print("\nDone!")
	df_all = pd.concat(datasets, ignore_index=True)
	return df_all

def make_sum(print_lable, files, csv = False):
	Run = load_data(print_lable, files)
	if csv == True:
		Run.to_csv(print_lable + ".csv", index=False)
	Run_sum = []
	for k in C_names:
		Run_sum.append(Run[k].sum())
	print(Run_sum)
	return Run_sum

if __name__ == "__main__":
	data_path = "/lustre/cms/store/user/mbuonsan/"
	
	files_2022C = [
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraC_stream0_Mini_v3/230507_105546/0000",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraC_stream1_Mini_v3/230507_105617/0000",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraC_stream2_Mini_v3/230507_105648/0000",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraC_stream3_Mini_v3/230507_105718/0000",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraC_stream4_Mini_v3/230507_105748/0000",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraC_stream5_Mini_v3/230507_105817/0000",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraC_stream6_Mini_v3/230507_105847/0000",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraC_stream7_Mini_v3/230507_105917/0000"
	]

	files_2022D = [
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD_stream0_Mini_v3/230507_105929/0000",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD_stream1_Mini_v3/230507_105959/0000",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD_stream2_Mini_v3/230507_110030/0000",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD_stream3_Mini_v3/230507_110101/0000",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD_stream4_Mini_v3/230507_110135/0000",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD_stream5_Mini_v3/230507_110209/0000",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD_stream6_Mini_v3/230507_110239/0000",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD_stream7_Mini_v3/230507_110308/0000"
	]

	files_2022E = [
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraE_stream0_Mini_v3/230507_110320/0000",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraE_stream1_Mini_v3/230507_110348/0000",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraE_stream2_Mini_v3/230507_110418/0000",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraE_stream3_Mini_v3/230507_110448/0000",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraE_stream4_Mini_v3/230507_110518/0000",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraE_stream5_Mini_v3/230507_110549/0000",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraE_stream6_Mini_v3/230507_110619/0000",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraE_stream7_Mini_v3/230507_110649/0000"
	]

	files_2022F = [
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraF_stream0_Mini_v3/230507_110700/0000",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraF_stream1_Mini_v3/230507_110734/0000",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraF_stream2_Mini_v3/230507_110806/0000",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraF_stream3_Mini_v3/230507_110838/0000",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraF_stream4_Mini_v3/230507_110908/0000",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraF_stream5_Mini_v3/230507_110939/0000",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraF_stream6_Mini_v3/230507_111009/0000",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraF_stream7_Mini_v3/230507_111039/0000",
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraF_stream0_Mini_v3/230507_110700/0001",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraF_stream1_Mini_v3/230507_110734/0001",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraF_stream2_Mini_v3/230507_110806/0001",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraF_stream3_Mini_v3/230507_110838/0001",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraF_stream4_Mini_v3/230507_110908/0001",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraF_stream5_Mini_v3/230507_110939/0001",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraF_stream6_Mini_v3/230507_111009/0001",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraF_stream7_Mini_v3/230507_111039/0001"
	]

	files_2022G = [
		"ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraG_stream0_Mini_v3/230507_111050/0000",
		"ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraG_stream1_Mini_v3/230507_111120/0000",
		"ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraG_stream2_Mini_v3/230507_111149/0000",
		"ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraG_stream3_Mini_v3/230507_111218/0000",
		"ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraG_stream4_Mini_v3/230507_111248/0000",
		"ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraG_stream5_Mini_v3/230507_111319/0000",
		"ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraG_stream6_Mini_v3/230507_111352/0000",
		"ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraG_stream7_Mini_v3/230507_111424/0000"
	]

	
	files_Run2022C = [data_path + i for i in files_2022C]
	files_Run2022D = [data_path + i for i in files_2022D]
	files_Run2022E = [data_path + i for i in files_2022E]
	files_Run2022F = [data_path + i for i in files_2022F]
	files_Run2022G = [data_path + i for i in files_2022G]

	files_2022_MC = [
		"DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_postE/230507_103348/0000",
		"DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_preE/230507_103411/0000",
	]

	files_Run2022_MC = [data_path + i for i in files_2022_MC]
	
	
	if data == True:
		R22C_sum = make_sum("Run_22C", files_Run2022C, csv = False)
		R22D_sum = make_sum("Run_22D", files_Run2022D, csv = False)
		R22E_sum = make_sum("Run_22E", files_Run2022E, csv = False)
		R22F_sum = make_sum("Run_22F", files_Run2022F, csv = False)
		R22G_sum = make_sum("Run_22G", files_Run2022G, csv = False)
		#R23C_v4_sum = make_sum("Run_23C_v4", files_Run2023C_v4, csv = False)

		list = [R22C_sum, R22D_sum, R22E_sum, R22F_sum, R22G_sum]
		df_out = pd.DataFrame(list, columns=C_names)
		df_out['Index'] = ["Run_22C", "Run_22D", "Run_22E", "Run_22F", "Run_22G"]
		column_order = ['Index'] + [col for col in df_out if col != 'Index']
		df_out = df_out[column_order]
		df_out.to_csv('Post_Ntuple_Data.csv', index=False)
	else:
		Run_2022_MC = make_sum("MC_2022", files_Run2022_MC, csv = False)
		list = [Run_2022_MC]
		print("********")
		df_out = pd.DataFrame(list, columns=C_names)
		df_out.to_csv('Post_Ntuple_MC.csv', index=False)







	
