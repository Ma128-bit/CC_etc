import ROOT
ROOT.gROOT.SetBatch(True)
import pandas as pd
from file_locations import *

def MC_y(era_name):
    tmc = ROOT.TChain("FinalTree")
    tmc.Add("ROOTFiles/AllControl.root")
    
    h_MC = ROOT.TH1F("h_MC", "h_MC", 42, 1.65, 2.05)
    tmc.Draw("tripletMass>>h_MC", "control_weight*(ID==\""+era_name+"\")", "N")
    
    xMin = h_MC.GetXaxis().GetXmin()
    xMax = h_MC.GetXaxis().GetXmax()
    nBins = h_MC.GetNbinsX()
    
    x = ROOT.RooRealVar("x", "x", xMin, xMax)
    x.setBins(nBins)
    
    data = ROOT.RooDataHist("data", h_MC.GetTitle(), ROOT.RooArgSet(x), ROOT.RooFit.Import(h_MC, False))
    
    mGCB = ROOT.RooRealVar("mean", "meanCB", 1.97, 1.95, 2.0)
    sigma1CB = ROOT.RooRealVar("#sigma_{CB}", "sigma1CB", 0.02, 0.01, 0.1)
    sig2CBPdf = ROOT.RooGaussian("sig2CBPdf", "sig2CBPdf", x, mGCB, sigma1CB)
    
    nSig = ROOT.RooRealVar("nSig", "Number of signal candidates", h_MC.GetEntries(), 1., 1e+6)
    
    # Fondo:
    d1 = ROOT.RooRealVar("d_{1}", "d1", -0.1, -10, 10)
    #d2 = ROOT.RooRealVar("d_{2}", "d2", -0.1, -10, 10)
    bkgPDF = ROOT.RooChebychev("bkgPDF", "bkgPDF", x, ROOT.RooArgSet(d1))
    nBkg = ROOT.RooRealVar("nBkg", "Bkg component", 1., 1., 1e+6)
    
    totalPDF = ROOT.RooAddPdf("totalPDF", "totalPDF", ROOT.RooArgList(sig2CBPdf, bkgPDF), ROOT.RooArgList(nSig, nBkg))
    #totalPDF = ROOT.RooAddPdf("totalPDF", "totalPDF", ROOT.RooArgList(sig2CBPdf), ROOT.RooArgList(nSig))
    r = totalPDF.fitTo(data, ROOT.RooFit.Extended(True), ROOT.RooFit.Save(True))
    
    xframe = x.frame()  # definisco frame
    xframe.SetTitle("")
    xframe.SetXTitle("2mu +1trk inv. mass (GeV)")
    data.plotOn(xframe)
    totalPDF.plotOn(xframe, ROOT.RooFit.Components(ROOT.RooArgSet(sig2CBPdf)), ROOT.RooFit.LineColor(ROOT.kRed))
    totalPDF.plotOn(xframe, ROOT.RooFit.Components(ROOT.RooArgSet(bkgPDF)), ROOT.RooFit.LineColor(ROOT.kGreen), ROOT.RooFit.LineStyle(ROOT.kDashed))
    totalPDF.plotOn(xframe)

    c1 = ROOT.TCanvas("c1", "c1", 900, 900)
    c1.Divide(1, 2)
    
    # plotto oltre al fit anche le pull:
    xframePull = x.frame()  # creo un nuovo frame
    xframePull.SetTitle("Pulls bin-by-bin")
    xframePull.SetXTitle("2mu +1trk inv. mass (GeV)")
    xframePull.SetYTitle("Pulls")
    xframePull.addObject(xframe.pullHist(), "p")
    xframePull.SetMinimum(-4)
    xframePull.SetMaximum(4)
    c1.cd(2)  # Qui disegno le pull
    ROOT.gPad.SetPad(0., 0., 1., 0.3)
    xframePull.Draw()
    line = ROOT.TLine(xMin, 0., xMax, 0.)
    line.SetLineColor(2)
    line.Draw("same")
    c1.cd(1)  # qui il grafico con il fit
    ROOT.gPad.SetPad(0., 0.3, 1., 1.)
    xframe.Draw()
    c1.SaveAs("Mass_Fits/MC_"+era_name+".png")
    

    # Integrale
    x.setRange("signal", 1.93, 2.01)
    sig_int = sig2CBPdf.createIntegral(x, ROOT.RooFit.NormSet(x), ROOT.RooFit.Range("signal"))
    ysig = sig_int.getVal() * nSig.getVal()
    ysig_e2 = pow(sig_int.getPropagatedError(r) * nSig.getVal(), 2) + pow(sig_int.getVal() * nSig.getError(), 2)
    ysig_e = ROOT.TMath.Sqrt(ysig_e2)

    new_line = pd.DataFrame({'MC': [era_name], 
                             'Yield': [ysig], 
                             'Error': [ysig_e]})

    return new_line

if __name__ == "__main__":
    df = pd.DataFrame(columns=['MC', 'Yield', 'Error'])
    
    new_line = MC_y("DsPhiPi_preE")
    df = pd.concat([df, new_line], ignore_index=True)
    
    new_line = MC_y("DsPhiPi_postE")
    df = pd.concat([df, new_line], ignore_index=True)
    
    df.to_csv('Mass_Fits/Yield_MC.csv', index=False)
