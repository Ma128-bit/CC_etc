import os
import ROOT
ROOT.gROOT.SetBatch(True)
import subprocess
import argparse
import pandas as pd
from ROOT import *
from file_locations import *

var = ["cLP", "tKink", "segmComp", "fv_nC", "d0sig", "fv_dphi3D", "fv_d3Dsig", "mindca_iso", "trkRel", "d0sig_max", "MVASoft1", "MVASoft2","Ptmu3", "fv_d3D"]

invmass_SB = "(tripletMass<1.8 && tripletMass>1.70)"
invmass_peak = "(tripletMass<2.01 && tripletMass>1.93)"
binning_mass = "(65, 1.60, 2.02)"

binning_dict = {
    "fv_d3D": "(100,0,1.5)",
    "Ptmu1": "(60,0,30)",
    "Ptmu2": "(60,0,30)",
    "Ptmu3": "(60,0,20)",
    "Etamu1": "(30,0,2.5)",
    "Etamu2": "(30,0,2.5)",
    "Etamu3": "(30,0,2.5)",
    "Pmu3": "(100,0,50)",
    "cLP": "(60,0,20)",
    "segmComp": "(100,-0.1,1.1)",
    "tKink": "(50,0,50)",
    "fv_nC": "(50,-0.1,5.1)",
    "d0sig": "(36,-0.1,18)",
    "d0sig_max": "(36,-0.1,30)",
    "mindca_iso": "(40,0,0.4)",
    "trkRel": "(40,0.05,1.1)",
    "tripletMassReso": "(80,0,0.02)",
    "fv_dphi3D": "(42,-0.01,0.20)",
    "fv_d3Dsig": "(50,-0.1,80)",
    "MVASoft1": "(50,0.2,0.8)",
    "MVASoft2": "(50,0.2,0.8)"
}

def fit_bkg(h1):
    x = RooRealVar("x", "2mu+1trk inv. mass (GeV)", 1.65, 2.05)
    x.setBins(40)
    datahist = RooDataHist("datahist", h1.GetTitle(), RooArgSet(x), RooFit.Import(h1, ROOT.kFALSE))

    x.setRange("R1", 1.70, 1.80)
    x.setRange("R2", 1.93, 2.01)

    gamma = RooRealVar("#Gamma", "Gamma", -1, -2.0, -1e-2)
    exp_bkg = RooExponential("exp_bkg", "exp_bkg", x, gamma)
    exp_bkg.fitTo(datahist, RooFit.Range("R1"))
    fsigregion_bkg = exp_bkg.createIntegral(x, RooFit.NormSet(x), RooFit.Range("R2"))
    fbkgregion_bkg = exp_bkg.createIntegral(x, RooFit.NormSet(x), RooFit.Range("R1"))
    return h1.GetEntries()*fsigregion_bkg/fbkgregion_bkg


def control_plots(file_name, year):
    if not os.path.exists("Control_Plots"):
        subprocess.run(["mkdir", "Control_Plots"])
    
    # Data ALL
    data = TChain("FinalTree")
    data.Add(data)
    
    for k in range(len(var)):
        varname = var[k]
        s = str(k)
        binning = binning_dict[varname]
        data.Draw(varname + ">>hdata_bkg" + s+ binning, "control_weight*(isMC==0 &&" + invmass_SB+")")
        data.Draw(varname + ">>hdata_sig" + s + binning, "control_weight*(isMC==0 &&" +invmass_peak+")")
        hdata_bkg = TH1F(gDirectory.Get("hdata_bkg" + s))
        hdata_sig = TH1F(gDirectory.Get("hdata_sig" + s))
        
        data.Draw(varname + ">>hMC_sig" + s + binning, "control_weight*(isMC>0 &&" +invmass_peak+")")
        hMC_sig = TH1F(gDirectory.Get("hMC_sig" + s))

        c2 = TCanvas("c2", "c2", 150, 10, 990, 660)
        pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0)
        pad1.SetGridx()
        pad1.Draw()
        pad1.cd()
        hMC_sig.SetTitle(varname)
        
        # Scaling the SB distribution to the number of background events in 1.93,2.01
        normSB = hdata_bkg.GetEntries()
        scale = fit_bkg(hdata_bkg)
        print(scale)
        hdata_bkg.Scale(scale / normSB)
        #print("Entries in hdata_sig before SB subtraction:", hdata_sig.GetEntries())
        hdata_sig.Add(hdata_bkg, -1)  # subtract h2 from h1: h1->Add(h2,-1)

        # Rescaling
        hdata_sig.Scale(hMC_sig.Integral() / hdata_sig.Integral())

        #print("Entries in hdata_sig after SB subtraction:", hdata_sig.GetEntries())
        #print("Entries in hMC_sig after rescaling:", hMC_sig.GetEntries())

        # Plot makeup
        Y_max = max(hMC_sig.GetMaximum(), hdata_sig.GetMaximum())
        Y_max = Y_max * 1.05
        hMC_sig.GetYaxis().SetRangeUser(0, Y_max)

        hMC_sig.GetYaxis().SetTitle("a.u.")
        hMC_sig.GetXaxis().SetTitle(varname)
        hMC_sig.GetYaxis().SetTitleSize(22)
        hMC_sig.GetYaxis().SetTitleFont(43)
        hMC_sig.GetYaxis().SetTitleOffset(1.25)

        hMC_sig.SetLineColor(kBlue)
        hMC_sig.SetLineWidth(3)
        hMC_sig.SetFillStyle(3004)
        hMC_sig.SetFillColor(kBlue)
        hdata_sig.SetLineColor(kRed)
        hdata_sig.SetLineWidth(3)
        hdata_sig.SetFillStyle(3005)
        hdata_sig.SetFillColor(kRed)

        hMC_sig.Draw("hist")
        hdata_sig.Draw("hist same")

        hMC_sig.SetStats(0)
        x_leg_left = 0.55
        x_leg_right = 0.90
        y_leg_left = 0.63
        y_leg_right = 0.90
        if varname == "segmComp" or varname == "MVASoft1" or varname == "MVASoft2":
            x_leg_left = 0.1
            x_leg_right = 0.45
        leg = TLegend(x_leg_left, y_leg_left, x_leg_right, y_leg_right)
        leg.AddEntry(hMC_sig, "MC DsPhiPi", "f")
        leg.AddEntry(hdata_sig, "data (SB subtracted)", "f")
        leg.Draw()

        # Lower plot will be in pad2
        c2.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.2)
        pad2.SetGridx()
        pad2.Draw()
        pad2.cd()

        # Define the ratio plot
        h_x_ratio = hdata_sig.Clone("h_x_ratio")
        h_x_ratio.Sumw2()
        h_x_ratio.Divide(hMC_sig)
        h_x_ratio.SetStats(0)

        # Ratio plot settings
        h_x_ratio.SetTitle("")  # Remove the ratio title
        h_x_ratio.GetYaxis().SetTitle("ratio data/MC")
        h_x_ratio.GetYaxis().SetRangeUser(-0.5, 2)

        h_x_ratio.SetLineColor(kBlack)
        h_x_ratio.GetYaxis().SetTitleSize(22)
        h_x_ratio.GetYaxis().SetTitleFont(43)
        h_x_ratio.GetYaxis().SetTitleOffset(1.25)
        h_x_ratio.GetYaxis().SetLabelFont(43)
        h_x_ratio.GetYaxis().SetLabelSize(15)

        # X axis ratio plot settings
        h_x_ratio.GetXaxis().SetTitle(varname)
        h_x_ratio.GetXaxis().SetTitleSize(22)
        h_x_ratio.GetXaxis().SetTitleFont(43)
        h_x_ratio.GetXaxis().SetTitleOffset(2.0)
        h_x_ratio.GetXaxis().SetLabelFont(43)
        h_x_ratio.GetXaxis().SetLabelSize(15)

        # Compute weighted average ratio
        mean = 0
        std_dev = 0
        for c in range(1, h_x_ratio.GetNbinsX() + 1):
            if h_x_ratio.GetBinContent(c) == 0 or h_x_ratio.GetBinError(c) == 0:
                continue
            mean += h_x_ratio.GetBinContent(c) / (h_x_ratio.GetBinError(c) * h_x_ratio.GetBinError(c))
            std_dev += 1 / (h_x_ratio.GetBinError(c) * h_x_ratio.GetBinError(c))
        mean = mean / std_dev
        std_dev = 1 / std_dev

        # Get mean value and error of ratio plot
        #print(var[k] + " Mean:", mean)
        #print(var[k] + " StdDev:", std_dev)

        # Draw line corresponding to mean value on ratio plot
        line = TLine()
        h_x_ratio.Draw("ep")
        line.SetLineWidth(2)
        line.SetLineColor(kRed)
        line.DrawLine(float(binning.split(',')[1]), 1, h_x_ratio.GetXaxis().GetXmax(), 1)
        h_x_ratio.Draw("same")

        c2.cd()
        c2.Update()
        c2.SaveAs("Control_Plots/" + varname + "_"+year+".png")
        del c2
        del pad2
        del pad1
        del line
        h_x_ratio.Delete();
        hdata_bkg.Delete();
        hdata_sig.Delete();
        hMC_sig.Delete(); 

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="--plots for control plots")
    parser.add_argument("--file", type=str, help="file name")
    parser.add_argument("--year", type=str, help="year (2022 or 2023)")
    args = parser.parse_args()
    file = args.file
    year = args.year
    control_plots(file, year)
