import ROOT
from ROOT import *
from file_locations import *

var = ["cLP", "tKink", "segmComp", "fv_nC", "d0sig", "fv_dphi3D", "fv_d3Dsig", "mindca_iso", "trkRel", "d0sig_max", "MVASoft1", "MVASoft2"]

invmass_SB = "(tripletMass<1.80 && tripletMass>1.70)"
invmass_peak = "(tripletMass<2.01 && tripletMass>1.93)"
binning_mass = "(65, 1.60, 2.02)"

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

def fit(ch, par, yield_vals, lumi, era="all"):
    ROOT.gROOT.SetBatch(ROOT.kTRUE)  # To run ROOT in batch mode    
    print("Total entries era", era, "=", ch.GetEntries())

    selez = "(Ptmu3 > 1.2 && ((Ptmu1>3.5 && Etamu1<1.2) || (Ptmu1>2.0 && Etamu1>=1.2 && Etamu1<=2.4)) && ((Ptmu2>3.5 && Etamu2<1.2) || (Ptmu2>2.0 && Etamu2>=1.2 && Etamu2<=2.4)))"

    h_tripletmass = ROOT.TH1F()
    h_tripletmass_bkg = ROOT.TH1F()
    h_tripletmass_sign = ROOT.TH1F()

    ch.Draw("tripletMass>>h_tripletmass"+binning_mass, selez)
    h_tripletmass = ROOT.gDirectory.Get("h_tripletmass")
    ch.Draw("tripletMass>>h_tripletmass_bkg"+binning_mass, invmass_SB + "&&" + selez)
    h_tripletmass_bkg = ROOT.gDirectory.Get("h_tripletmass_bkg")
    ch.Draw("tripletMass>>h_tripletmass_sign"+binning_mass, invmass_peak + "&&" + selez)
    h_tripletmass_sign = ROOT.gDirectory.Get("h_tripletmass_sign")

    x = RooRealVar("x", "2mu+1trk inv. mass (GeV)", 1.65, 2.05)
    x.setBins(int(binning_mass.split(',')[0][1:]))
    data = RooDataSet("data", h_tripletmass.GetTitle(), RooArgSet(x), RooFit.Import(h_tripletmass, ROOT.kFALSE))

    x.setRange("R1", 1.83, 1.89)
    x.setRange("R2", 1.93, 2.02)
    x.setRange("R3", 1.65, 1.84)
    x.setRange("R4", 1.89, 1.925)
    x.setRange("R5", 1.99, 2.02)
    x.setRange("R6", 1.65, 2.02)

    mGCB = RooRealVar("mean", "meanCB", 1.97, 1.95, 2.0)
    sigma1CB = RooRealVar("#sigma_{CB}", "sigma1CB", 0.02, 0.001, 0.1)
    alpha = RooRealVar("#alpha", "alpha", par[0], 0.5, 10.0)
    nSigma = RooRealVar("n1", "n1", par[1], 0.1, 25.0)
    sigCBPdf = RooGaussian("sigCBPdf", "sigCBPdf", x, mGCB, sigma1CB)

    sigCBPdf.fitTo(data, RooFit.Range("R2"))

    mGCB2 = RooRealVar("mean2", "meanCB2", 1.87, 1.85, 1.90)
    sigma2CB = RooRealVar("#sigma2_{CB}", "sigma2CB", 0.03, 0.001, 0.1)
    sig2CBPdf = RooGaussian("sig2CBPdf", "sig2CBPdf", x, mGCB2, sigma2CB)
    sig2CBPdf.fitTo(data, RooFit.Range("R1"))

    gamma = RooRealVar("#Gamma", "Gamma", -1, -2.0, -1e-2)
    bkgExpPdf = RooExponential("bkgExpPdf", "bkgExpPdf", x, gamma)
    bkgExpPdf.fitTo(data, RooFit.Range("R3,R4,R5"))

    nSig2 = RooRealVar("nSig", "Number of signal candidates", yield_vals[0], 1.0, 1e+6)
    nSig1 = RooRealVar("nSig2", "Number of signal 2 candidates", yield_vals[1], 1.0, 1e+6)
    nBkg = RooRealVar("nBkg", "Bkg component", yield_vals[2], 1.0, 1e+6)

    totalPDF = RooAddPdf("totalPDF", "totalPDF", RooArgList(sigCBPdf, sig2CBPdf, bkgExpPdf),
                         RooArgList(nSig2, nSig1, nBkg))

    r = totalPDF.fitTo(data, RooFit.Extended(ROOT.kTRUE), RooFit.Save(ROOT.kTRUE))

    xframe = x.frame()
    xframe.SetTitle("")
    xframe.SetXTitle("2mu +1trk inv. mass (GeV)")
    totalPDF.paramOn(xframe, RooFit.Parameters(RooArgSet(alpha, nSigma, nSig1, nSig2, nBkg)), RooFit.Layout(0.6, 0.9, 0.9))
    data.plotOn(xframe)
    totalPDF.plotOn(xframe, RooFit.Components(RooArgSet(sigCBPdf, sig2CBPdf)), RooFit.LineColor(ROOT.kRed), RooFit.LineStyle(ROOT.kDashed))
    totalPDF.plotOn(xframe, RooFit.Components(RooArgSet(bkgExpPdf)), RooFit.LineColor(ROOT.kGreen), RooFit.LineStyle(ROOT.kDashed))
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
    text = ROOT.TLatex(0.62, 0.91, "Data era " + era + "            L = " + lumi + "fb^{-1}")
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

    fsigregion_bkg = bkgExpPdf.createIntegral(x, RooFit.NormSet(x), RooFit.Range("signal"))
    fb = fsigregion_bkg.getVal()
    fb_err = fsigregion_bkg.getPropagatedError(r)

    nsigevents = fs * (nSig2.getVal() + nSig1.getVal() + nBkg.getVal()) - fb * nBkg.getVal()
    nsig_err = ROOT.TMath.Sqrt(
        fs_err**2 * (nSig2.getVal() + nSig1.getVal() + nBkg.getVal())**2 +
        (nSig2.getPropagatedError(r)**2 +
         nSig1.getPropagatedError(r)**2 +
         nBkg.getPropagatedError(r)**2) *
        fs**2 +
        fb_err**2 * nBkg.getVal()**2 +
        nBkg.getPropagatedError(r)**2 * fb**2
    )

    fsig = nsigevents / (fsigregion_model.getVal() * (nSig2.getVal() + nSig1.getVal() + nBkg.getVal()))

    with open('Inv_mass_plot/yield.txt', 'a') as file:
        file.write("Signal events in era", era, "=", nsigevents, "+-", nsig_err)

    chi2 = totalPDF.createChi2(data).getVal()
    ndof = int(binning_mass.split(',')[0][1:]) - 7
    chi = "#chi^{2}/NDOF = {:.2f}".format(chi2 / ndof)
    text3 = ROOT.TLatex(0.15, 0.77, chi)
    text3.SetNDC(ROOT.kTRUE)
    text3.SetTextSize(0.032)
    text3.SetTextFont(42)
    text3.Draw("same")

    if era == "all":
        with open('Inv_mass_plot/some_fit_results.txt', 'w') as file:
            file.write(fsigregion_bkg.getVal(), " ", nBkg.getVal())

    c1.SaveAs("Inv_mass_plot/inv_mass_{}.png".format(era))
    c1.Clear()
    fout.Close()

def Control_inv_mass():
    name = ["C", "D", "E", "F", "G"]
    lumi = ["0.25", "0.147", "0.29", "0.887", "0.153"]
    lumi_tot = "1.727"
    yield_vals = [[1500, 300, 22000], [1000, 250, 9000], [2000, 650, 23000], [7500, 1800, 60000], [800, 180, 10000]]
    par = [1., 1.]
    
    with open('Inv_mass_plot/yield.txt', 'w') as file:
        file.write('Yeald results per era:')
    
    ch_data = TChain("FinalTree")
    ch_data.Add(control_Run2022C)
    ch_data.Add(control_Run2022D)
    ch_data.Add(control_Run2022E)
    ch_data.Add(control_Run2022F)
    ch_data.Add(control_Run2022G)
    
    yy = [10000, 2000, 140000]
    fit(ch_data, par, yy, lumi_tot, "all")
    
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
    
