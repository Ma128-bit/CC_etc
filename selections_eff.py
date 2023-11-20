import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
import pickle
import xgboost as xgb
from sklearn.metrics import roc_curve, roc_auc_score
from pprint import pprint
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import ROOT
from ROOT import *

def load_histo(obj_name, file_name):
	"""Load ROOT data and turn tree into a pd dataframe"""
	print("Loading data from", file_name)
	f = uproot.open(file_name)
	obj = f[obj_name]
	num_entries = obj.values()
	num_entries = sum(num_entries)
	return num_entries

        
def load_data(obj_name, input_list):
	"""Load and merge ROOT trees with MVA data into a single dataset."""
	datasets = []
	j = 1
	for entry in input_list:
		print(j, "/",len(input_list), end='\r')
		j=j+1
		files = subprocess.check_output("find %s -type f -name '*root'" % entry, shell=True)
		for f in files.splitlines():
			datasets.append(load_histo(obj_name, f.decode()))
	print("Done!")
	sum = sum(datasets)
	return sum

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
	files_Run2022C = [data_path + i for i in files_2022C]

	histonames_CC= ["InitialPlots/hEvtCount", "PlotsAfterTrigger/hEvtCount", "PlotsAfterOnePFCand/hEvtCount", "PlotsAfterLooseMuon/hEvtCount", "PlotsAfterDiMuonCand/hEvtCount", "PlotsAfter2Mu1Track/hEvtCount", "PlotsAfterPhiPiCandSel/hEvtCount"]

	n = load_data(histonames_CC[0], files_Run2022C)

	print(n)






	
