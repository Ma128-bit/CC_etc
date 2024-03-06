from ROOT import gROOT, TH1F, RooDataHist, RooArgSet, RooExponential, RooRealVar, TChain, gDirectory, RooFit, kFALSE
gROOT.SetBatch(True)
import os, subprocess, argparse, draw_utilities
import pandas as pd
from file_locations import *

class ROOTDrawer(draw_utilities.ROOTDrawer):
    pass

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="--plots for control plots")
    parser.add_argument("--file", type=str, help="file name")
    parser.add_argument("--year", type=str, help="year (2022 or 2023)")
    args = parser.parse_args()
    file = args.file
    year = args.year
