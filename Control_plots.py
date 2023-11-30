import ROOT
import subprocess
import pandas as pd
from ROOT import *
from file_locations import *

var = ["cLP", "tKink", "segmComp", "fv_nC", "d0sig", "fv_dphi3D", "fv_d3Dsig", "mindca_iso", "trkRel", "d0sig_max", "MVASoft1", "MVASoft2"]

invmass_SB = "(tripletMass<1.80 && tripletMass>1.70)"
invmass_peak = "(tripletMass<2.01 && tripletMass>1.93)"
binning_mass = "(65, 1.60, 2.02)"

year = "2022"

Era2022 = {
    "C": control_Run2022C,
    "D": control_Run2022D,
    "E": control_Run2022E,
    "F": control_Run2022F,
    "G": control_Run2022G
}

lumi2022 = {
    "C": "0.25",
    "D": "0.147",
    "E": "0.29",
    "F": "0.887",
    "G": "0.153",
    "ToT": "1.727",
    "Pre_EE": "0.397",
    "Post_EE": "1.330"
}

binning_dict = {
    "Ptmu1": "(60,0,30)",
    "Ptmu2": "(60,0,30)",
    "Ptmu3": "(60,0,30)",
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

def fit(tree, year, lumi, era):
    ROOT.gROOT.SetBatch(ROOT.kTRUE)  # To run ROOT in batch mode    
    entries = tree.GetEntries()
    print("Total entries era", era, "=", entries)
    yields = [entries*0.05, entries*0.015, entries*0.7]

    selez = "(Ptmu3 > 1.2 && ((Ptmu1>3.5 && Etamu1<1.2) || (Ptmu1>2.0 && Etamu1>=1.2 && Etamu1<=2.4)) && ((Ptmu2>3.5 && Etamu2<1.2) || (Ptmu2>2.0 && Etamu2>=1.2 && Etamu2<=2.4)))"

    h_tripletmass = ROOT.TH1F()
    h_tripletmass_bkg = ROOT.TH1F()
    h_tripletmass_sign = ROOT.TH1F()

    tree.Draw("tripletMass>>h_tripletmass"+binning_mass, selez)
    h_tripletmass = ROOT.gDirectory.Get("h_tripletmass")
    tree.Draw("tripletMass>>h_tripletmass_bkg"+binning_mass, invmass_SB + "&&" + selez)
    h_tripletmass_bkg = ROOT.gDirectory.Get("h_tripletmass_bkg")
    tree.Draw("tripletMass>>h_tripletmass_sign"+binning_mass, invmass_peak + "&&" + selez)
    h_tripletmass_sign = ROOT.gDirectory.Get("h_tripletmass_sign")

    x = RooRealVar("x", "2mu+1trk inv. mass (GeV)", 1.65, 2.05)
    x.setBins(int(binning_mass.split(',')[0][1:]))
    data = RooDataHist("data", h_tripletmass.GetTitle(), RooArgSet(x), RooFit.Import(h_tripletmass, ROOT.kFALSE))

    x.setRange("R1", 1.65, 1.80)
    x.setRange("R2", 1.89, 1.925)
    x.setRange("R3", 1.99, 2.02)

    meanCB = RooRealVar("mean", "meanCB", 1.97, 1.95, 2.0)
    sigmaCB1 = RooRealVar("#sigma_{CB}", "sigmaCB1", 0.02, 0.001, 0.1)
    alpha1 = RooRealVar("#alpha1", "alpha1", 1.0, 0.5, 10.0)
    nSigma1 = RooRealVar("n1", "n1", 1.0, 0.1, 25.0)
    sig_right = RooCBShape("sig_right", "sig_right", x, meanCB, sigmaCB1, alpha1, nSigma1)

    meanCB2 = RooRealVar("mean2", "meanCB2", 1.87, 1.84, 1.89)
    sigmaCB2 = RooRealVar("#sigma2_{CB}", "sigmaCB2", 0.05, 0.001, 0.05)
    alpha2 = RooRealVar("#alpha2", "alpha2", 1.0, 0.5, 10.0)
    nSigma2 = RooRealVar("n2", "n2", 1.0, 0.1, 25.0)
    sig_left = RooCBShape("sig_left", "sig_left", x, meanCB2, sigmaCB2, alpha2, nSigma2)

    gamma = RooRealVar("#Gamma", "Gamma", -1, -2.0, -1e-2)
    exp_bkg = RooExponential("exp_bkg", "exp_bkg", x, gamma)
    exp_bkg.fitTo(data, RooFit.Range("R1,R2,R3"))

    nSig_right = RooRealVar("nSig_R", "Number of signal candidates", yields[0], 1.0, 1e+6)
    nSig_left = RooRealVar("nSig_L", "Number of signal 2 candidates", yields[1], 1.0, 1e+6)
    nBkg = RooRealVar("nBkg", "Bkg component", yields[2], 1.0, 1e+6)

    totalPDF = RooAddPdf("totalPDF", "totalPDF", RooArgList(sig_right, sig_left, exp_bkg), RooArgList(nSig_right, nSig_left, nBkg))

    r = totalPDF.fitTo(data, RooFit.Extended(ROOT.kTRUE), RooFit.Save(ROOT.kTRUE))

    xframe = x.frame()
    xframe.SetTitle("")
    xframe.SetXTitle("2mu +1trk inv. mass (GeV)")
    #totalPDF.paramOn(xframe, RooFit.Parameters(RooArgSet(alpha2, nSigma2, sigmaCB2, meanCB2, nSig_left, nSig_right, nBkg)), RooFit.Layout(0.6, 0.9, 0.9))
    data.plotOn(xframe)
    totalPDF.plotOn(xframe, RooFit.Components(RooArgSet(sig_right, sig_left)), RooFit.LineColor(ROOT.kRed), RooFit.LineStyle(ROOT.kDashed))
    totalPDF.plotOn(xframe, RooFit.Components(RooArgSet(exp_bkg)), RooFit.LineColor(ROOT.kGreen), RooFit.LineStyle(ROOT.kDashed))
    totalPDF.plotOn(xframe)

    c1 = ROOT.TCanvas("c1", "c1", 900, 900)
    c1.Divide(1, 2)

    xframePull = x.frame()
    xframePull.SetTitle("Pulls bin-by-bin")
    xframePull.SetXTitle("2mu +1trk inv. mass (GeV)")
    xframePull.SetYTitle("Pulls")
    xframePull.addObject(xframe.pullHist(), "p")
    xframePull.SetMinimum(-4)
    xframePull.SetMaximum(4)
    c1.cd(2)
    ROOT.gPad.SetPad(0., 0., 1., 0.3)
    xframePull.Draw()

    c1.cd(1)
    ROOT.gPad.SetPad(0., 0.3, 1., 1.)
    xframe.Draw()
    
    lable_era = ""
    if era != year:
        lable_era = "Data Era " + era
    else:
        lable_era = "Data " + era
    text = ROOT.TLatex(0.62, 0.91, lable_era + "            L = " + lumi + "fb^{-1}")
    text.SetNDC(ROOT.kTRUE)
    text.SetTextSize(0.032)
    text.SetTextFont(42)
    text.Draw("same")
    text2 = ROOT.TLatex(0.15, 0.81, "#bf{CMS Preliminary}")
    text2.SetNDC(ROOT.kTRUE)
    text2.SetTextSize(0.032)
    text2.SetTextFont(42)
    text2.Draw("same")

    x.setRange("signal", 1.93, 2.01)
    x.setRange("sideband", 1.7, 1.8)

    fsigregion_model = totalPDF.createIntegral(x, RooFit.NormSet(x), RooFit.Range("signal"))
    fs = fsigregion_model.getVal()
    fs_err = fsigregion_model.getPropagatedError(r)

    fsidebandregion_model = totalPDF.createIntegral(x, RooFit.NormSet(x), RooFit.Range("sideband"))

    fsigregion_bkg = exp_bkg.createIntegral(x, RooFit.NormSet(x), RooFit.Range("signal"))
    fb = fsigregion_bkg.getVal()
    fb_err = fsigregion_bkg.getPropagatedError(r)

    nsigevents = fs * (nSig_right.getVal() + nSig_left.getVal() + nBkg.getVal()) - fb * nBkg.getVal()
    nsig_err = ROOT.TMath.Sqrt(
        fs_err**2 * (nSig_right.getVal() + nSig_left.getVal() + nBkg.getVal())**2 +
        (nSig_right.getPropagatedError(r)**2 +
         nSig_left.getPropagatedError(r)**2 +
         nBkg.getPropagatedError(r)**2) *
        fs**2 +
        fb_err**2 * nBkg.getVal()**2 +
        nBkg.getPropagatedError(r)**2 * fb**2
    )

    fsig = nsigevents / (fsigregion_model.getVal() * (nSig_right.getVal() + nSig_left.getVal() + nBkg.getVal()))
    # Save in pd dataframe
    new_line = pd.DataFrame({'Era': [era], 
                             'Yeald': [nsigevents], 
                             'Error': [nsig_err]})
    
    chi2 = totalPDF.createChi2(data).getVal()
    ndof = int(binning_mass.split(',')[0][1:]) - 7
    print("chi2: ", chi2)
    print("ndof: ", ndof)
    chi2_ndof = chi2/ndof
    chi2_txt = "#chi^{2}/NDOF = " + "{:.2f}".format(chi2_ndof)
    text3 = ROOT.TLatex(0.15, 0.77, chi2_txt)
    text3.SetNDC(ROOT.kTRUE)
    text3.SetTextSize(0.032)
    text3.SetTextFont(42)
    text3.Draw("same")
    
    if era == year:
        with open('Mass_Fits/some_fit_results.txt', 'w') as file:
            file.write(f"{fsigregion_bkg.getVal()} {nBkg.getVal()}")

    c1.SaveAs("Mass_Fits/Fit_{}.png".format(era), "png -dpi 600")
    c1.Clear()
    return new_line

def Control_inv_mass():
    subprocess.run(["mkdir", "Mass_Fits"])
    df = pd.DataFrame(columns=['Era', 'Yeald', 'Error'])
    ch_data = TChain("FinalTree")
    
    if year == "2022":
        Eras = Era2022
        Lumi_values = lumi2022
        ch_data_pre = TChain("FinalTree")
        ch_data_post = TChain("FinalTree")
    
    for era, data in Eras.items():
        file = ROOT.TFile(data, "READ")
        tree = file.Get("FinalTree")
        new_line = fit(tree, year, Lumi_values[era], era)
        df = pd.concat([df, new_line], ignore_index=True)
        if year == "2022" and (era == "C" or era == "D"):
            ch_data_pre.Add(data)
        if year == "2022" and (era == "E" or era == "F" or era == "G"):
            ch_data_post.Add(data)
        ch_data.Add(data)
        del tree
    
    new_line = fit(ch_data, year, Lumi_values["ToT"], year)
    df = pd.concat([df, new_line], ignore_index=True)
    
    if year == "2022":
        new_line = fit(ch_data_pre, year, Lumi_values["Pre_EE"], "Pre_EE")
        df = pd.concat([df, new_line], ignore_index=True)
        del ch_data_pre
        new_line = fit(ch_data_post, year, Lumi_values["Post_EE"], "Post_EE")
        df = pd.concat([df, new_line], ignore_index=True)
        del ch_data_post
    
    df.to_csv('Mass_Fits/Yeald.csv', index=False)
    del ch_data

def control_plot_2022():
    lumi = 1.754213258  # recorded lumi by HLT_DoubleMu3_Trk_Tau3mu_v*
    lumi_preE = 0.403852348  # recorded lumi by HLT_DoubleMu3_Trk_Tau3mu_v*
    lumi_postE = 1.35036091  # recorded lumi by HLT_DoubleMu3_Trk_Tau3mu_v*
    xsection_mc_postE = 1.103e10  # Ds Production Cross section
    xsection_mc_preE = 1.106e10  # Ds Production Cross section
    BR = 1.29e-5  # Branching ratio Ds to Phi Pi

    # Data ALL
    ch_data = TChain("FinalTree")
    ch_data.Add(control_Run2022C)
    ch_data.Add(control_Run2022D)
    ch_data.Add(control_Run2022E)
    ch_data.Add(control_Run2022F)
    ch_data.Add(control_Run2022G)

    # MC ALL
    tmc_1 = TChain("FinalTree")
    tmc_1.Add(MC2022_DsPhiPi_pre)
    n1 = tmc_1.GetEntries()
    tmc_2 = TChain("FinalTree")
    tmc_2.Add(MC2022_DsPhiPi_post)
    n2 = tmc_2.GetEntries()
    N_MC = n1 + n1
    print("N_MC: ", N_MC)
    print("n1: ", n1)
    print("n2: ", n2)

    invmass_SB = "(tripletMass<1.80 && tripletMass>1.70)"
    invmass_peak = "(tripletMass<2.01 && tripletMass>1.93)"
    binning_mass = "(42, 1.60, 2.02)"

    for k in range(len(var)):
        varname = var[k]
        s = str(k)
        binning = binning_dict[varname]

        ch_data.Draw(varname + ">>hdata_bkg" + s+ binning, invmass_SB)
        ch_data.Draw(varname + ">>hdata_sgn" + s + binning, invmass_peak)
        tmc_1.Draw(varname + ">>hmc_sgn" + s + binning, invmass_peak)
        tmc_2.Draw(varname + ">>hmc_sgn2" + s + binning, invmass_peak)

        hdata_bkg = TH1F(gDirectory.Get("hdata_bkg" + s))
        hdata_sgn = TH1F(gDirectory.Get("hdata_sgn" + s))
        hmc_sgn = TH1F(gDirectory.Get("hmc_sgn" + s))
        hmc_sgn2 = TH1F(gDirectory.Get("hmc_sgn2" + s))

        c2 = TCanvas("c2", "c2", 150, 10, 990, 660)
        pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0)
        pad1.SetGridx()
        pad1.Draw()
        pad1.cd()
        hmc_sgn.SetTitle(varname)
        hmc_sgn2.SetTitle(varname)

        # Normalizzazione MC preE
        normMC = hmc_sgn.GetEntries()
        wNorm = lumi_preE * xsection_mc_preE * BR / N_MC
        hmc_sgn.Scale(wNorm)

        # Normalizzazione MC postE
        normMC2 = hmc_sgn2.GetEntries()
        # Normalizing Monte Carlo
        wNorm2 = lumi_postE * xsection_mc_postE * BR / N_MC
        hmc_sgn2.Scale(wNorm2)

        # Unisco i due MC
        hmc_sgn.Add(hmc_sgn2)
        # Scaling the SB distribution to the number of background events in 1.93,2.01
        normSB = hdata_bkg.GetEntries()

        with open("Inv_mass_plot/some_fit_results.txt") as fin:
            fsigregion_bkg_val = float(fin.readline())
            nbkg_val = float(fin.readline())

        hdata_bkg.Scale(fsigregion_bkg_val * nbkg_val / normSB)

        print("Entries in hdata_sgn before SB subtraction:", hdata_sgn.GetEntries())
        hdata_sgn.Add(hdata_bkg, -1)  # subtract h2 from h1: h1->Add(h2,-1)

        # Rescaling
        hdata_sgn.Scale(hmc_sgn.Integral() / hdata_sgn.Integral())

        print("Entries in hdata_sgn after SB subtraction:", hdata_sgn.GetEntries())
        print("Entries in hmc_sgn after rescaling:", hmc_sgn.GetEntries())

        # Plot makeup
        Y_max = max(hmc_sgn.GetMaximum(), hdata_sgn.GetMaximum())
        Y_max = Y_max * 1.05
        hmc_sgn.GetYaxis().SetRangeUser(0, Y_max)

        hmc_sgn.GetYaxis().SetTitle("a.u.")
        hmc_sgn.GetYaxis().SetTitleSize(22)
        hmc_sgn.GetYaxis().SetTitleFont(43)
        hmc_sgn.GetYaxis().SetTitleOffset(1.25)

        hmc_sgn.SetLineColor(kBlue)
        hmc_sgn.SetLineWidth(3)
        hmc_sgn.SetFillStyle(3004)
        hmc_sgn.SetFillColor(kBlue)
        hdata_sgn.SetLineColor(kRed)
        hdata_sgn.SetLineWidth(3)
        hdata_sgn.SetFillStyle(3005)
        hdata_sgn.SetFillColor(kRed)

        hmc_sgn.Draw("hist")
        hdata_sgn.Draw("hist same")

        hmc_sgn.SetStats(0)
        x_leg_left = 0.55
        x_leg_right = 0.90
        y_leg_left = 0.63
        y_leg_right = 0.90
        if varname == "segmComp" or varname == "MVASoft1" or varname == "MVASoft2":
            x_leg_left = 0.1
            x_leg_right = 0.45
        leg = TLegend(x_leg_left, y_leg_left, x_leg_right, y_leg_right)
        leg.AddEntry(hmc_sgn, "MC DsPhiPi", "f")
        leg.AddEntry(hdata_sgn, "data (SB subtracted)", "f")
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
        h_x_ratio = hdata_sgn.Clone("h_x_ratio")
        h_x_ratio.Sumw2()
        h_x_ratio.Divide(hmc_sgn)
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
        print(var[k] + " Mean:", mean)
        print(var[k] + " StdDev:", std_dev)

        # Draw line corresponding to mean value on ratio plot
        line = TLine()
        h_x_ratio.Draw("ep")
        line.DrawLine(0, mean, h_x_ratio.GetXaxis().GetXmax(), mean)
        h_x_ratio.Draw("same")

        c2.cd()
        c2.Update()
        c2.SaveAs("control_plots/" + varname + "_.png")

if __name__ == "__main__": 
    Control_inv_mass()
    
