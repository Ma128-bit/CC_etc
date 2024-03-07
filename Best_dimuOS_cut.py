from ROOT import gROOT, TH1F, RooDataHist, RooArgSet, RooExponential, RooRealVar, TChain, gDirectory, RooFit, kFALSE
gROOT.SetBatch(True)
import os, subprocess, argparse, draw_utilities, math
import pandas as pd
from file_locations import *

class ROOTDrawer(draw_utilities.ROOTDrawer):
    pass

sigma_phi = [0.011,0.015,0.018]
sigma_omega = [0.012,0.015,0.022]
sigma_tau = [0.011, 0.018, 0.026]

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="--plots for control plots")
    parser.add_argument("--file", type=str, help="file name")
    parser.add_argument("--year", type=str, help="year (2022 or 2023)")
    args = parser.parse_args()
    file = args.file
    year = args.year
    
    data = TChain("FinalTree")
    data.Add(file)

    canvas = ROOTDrawer(SetGridx = True, SetLogY= True)
    
    for j in range(3):
        sig = []
        bkg = []
        AMS = []
        for i in range(0,11):
            s = str((j+1)*(i+1))
            data.Draw("tripletMass>>h_bkg" +s+ "(52, 1.6, 2)", "(isMC==0 && abs(1.777 - tripletMass)>"+ str(3*sigma_tau[j]) + "&& category=="+ str(j) + "&& abs(dimu_OS1 - 0.7826)>"+str((i/2)*0.01)  + "&& abs(dimu_OS2 - 0.7826)>"+str((i/2)*0.01)  +")")
            data.Draw("tripletMass>>h_sig" +s+ "(52, 1.6, 2)", "(isMC>0" + "&& category=="+ str(j) + "&& abs(dimu_OS1 - 0.7826)>"+str((i/2)*0.01)  + "&& abs(dimu_OS2 - 0.7826)>"+str((i/2)*0.01)  +")")
            h_sig = gDirectory.Get("h_sig"+s)
            h_bkg = gDirectory.Get("h_bkg"+s)
            S=h_sig.Integral()
            B=h_bkg.Integral()*6*sigma_tau[j]/(0.4-6*sigma_tau[j])
            sig.append(S)
            bkg.append(B)
            AMS.append(S/B)
            #AMS.append(math.sqrt(2*((S+B)*math.log(1+S/B) - S)))
            
        hist = TH1F("AMScat"+str(j), "AMS cat "+ str(j), 11, -0.25, 5.25)
        for i in range(len(AMS)):
            hist.SetBinContent(i+1, AMS[i])
        canvas.HaddTH1(hist, Color=j+2, SetXName="N. #sigma", SetYName="a.u.", label="Category "+str(j), DrawOpt = "P")
        del hist

    canvas.MakeLegend()
    canvas.Save("prova.png", era=int(year), extra="Preliminary")
    print(canvas.YRange)
    
