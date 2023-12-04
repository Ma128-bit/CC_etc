import ROOT

def RM_Branch(oldfile, newfile, s="tau3mu"):
    oldtree = oldfile.Get("FinalTree")
    oldtree.SetBranchStatus("*", 0)

    branches_to_keep = ["isMC", "lumi", "run", "evt", "puFactor", "DeltaR_max", "DeltaZ_max", "Pmu3", "cLP", "tKink",
                         "segmComp", "tripletMass", "fv_nC", "fv_dphi3D", "fv_d3D", "fv_d3Dsig", "d0", "d0sig",
                         "d0sig_max", "mindca_iso", "trkRel", "Ptmu1", "Etamu1", "Ptmu2", "Etamu2", "Ptmu3", "Etamu3",
                         "Pmu1", "Pmu2", "P_tripl", "Pt_tripl", "Eta_tripl", "MVA1", "MVA2", "MVASoft1", "MVASoft2",
                         "ChargeMu1", "ChargeMu2", "ChargeMu3", "nVtx"]

    if s == "tau3mu":
        branches_to_keep.extend(["tripletMassReso", "category", "MVA3", "MVASoft3", "dimu_OS1", "dimu_OS2"])

    for branch in branches_to_keep:
        oldtree.SetBranchStatus(branch, 1)

    newtree = oldtree.CloneTree(0)
    newtree.CopyEntries(oldtree)
    newfile.Write()

def Add_Branch(f, _h, _h1, Tipe="Data"):
    T = f.Get("FinalTree")
    weight = ROOT.Double(99.0)
    weight_MC = ROOT.Double(99.0)
    weight_MC2 = ROOT.Double(99.0)
    mu1_muSF = ROOT.Double(1.0)
    mu1_muSF_err = ROOT.Double(0.0)
    mu2_muSF = ROOT.Double(1.0)
    mu2_muSF_err = ROOT.Double(0.0)
    mu3_muSF = ROOT.Double(1.0)
    mu3_muSF_err = ROOT.Double(0.0)
    weight_nVtx = ROOT.Double(99.0)
    weight_nVtx_err = ROOT.Double(0.0)
    weight_CC = ROOT.Double(99.0)
    weight_CC_err = ROOT.Double(0.0)

    b_weight = T.Branch("weight", weight, "weight/D")
    b_weight_MC = T.Branch("weight_MC", weight_MC, "weight_MC/D")
    b_weight_MC2 = T.Branch("weight_MC2", weight_MC2, "weight_MC2/D")
    b_mu1_muSF = T.Branch("mu1_muSF", mu1_muSF, "mu1_muSF/D")
    b_mu1_muSF_err = T.Branch("mu1_muSF_err", mu1_muSF_err, "mu1_muSF_err/D")
    b_mu2_muSF = T.Branch("mu2_muSF", mu2_muSF, "mu2_muSF/D")
    b_mu2_muSF_err = T.Branch("mu2_muSF_err", mu2_muSF_err, "mu2_muSF_err/D")
    b_mu3_muSF = T.Branch("mu3_muSF", mu3_muSF, "mu3_muSF/D")
    b_mu3_muSF_err = T.Branch("mu3_muSF_err", mu3_muSF_err, "mu3_muSF_err/D")
    b_weight_nVtx = T.Branch("weight_nVtx", weight_nVtx, "weight_nVtx/D")
    b_weight_nVtx_err = T.Branch("weight_nVtx_err", weight_nVtx_err, "weight_nVtx_err/D")
    b_weight_CC = T.Branch("weight_CC", weight_CC, "weight_CC/D")
    b_weight_CC_err = T.Branch("weight_CC_err", weight_CC_err, "weight_CC_err/D")

    pt1, eta1, pt2, eta2, pt3, eta3 = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    Vtx = ROOT.Double(0)

    T.SetBranchAddress("Ptmu1", pt1)
    T.SetBranchAddress("Ptmu2", pt2)
    T.SetBranchAddress("Ptmu3", pt3)
    T.SetBranchAddress("Etamu1", eta1)
    T.SetBranchAddress("Etamu2", eta2)
    T.SetBranchAddress("Etamu3", eta3)
    T.SetBranchAddress("nVtx", Vtx)

    nentries = T.GetEntries()

    for i in range(nentries):
        T.GetEntry(i)

        if Tipe == "Data":
            weight = 1.0

        if Tipe == "Ds_preE":
            weight = (_h.GetBinContent(_h.FindBin(Vtx)) /
                      _h.GetBinError(_h.FindBin(Vtx))) if _h else 1.0

        if Tipe == "Ds_postE":
            weight = (_h.GetBinContent(_h.FindBin(Vtx)) /
                      _h.GetBinError(_h.FindBin(Vtx))) if _h else 1.0

        # Similar assignments for other Tipe values...

        b_weight.Fill()
        b_weight_MC.Fill()
        b_weight_MC2.Fill()
        b_mu1_muSF.Fill()
        b_mu2_muSF.Fill()
        b_mu3_muSF.Fill()
        b_mu1_muSF_err.Fill()
        b_mu2_muSF_err.Fill()
        b_mu3_muSF_err.Fill()
        b_weight_nVtx.Fill()
        b_weight_nVtx_err.Fill()
        b_weight_CC.Fill()
        b_weight_CC_err.Fill()

    T.Write("", ROOT.TObject.kOverwrite)
    del T

def GetMuonSF(_h, pt, eta, SF, SF_e):
    if _h.InheritsFrom("TH2"):
        if (_h.GetYaxis().GetXmin() < pt < _h.GetYaxis().GetXmax() and
                _h.GetXaxis().GetXmin() < abs(eta) < _h.GetXaxis().GetXmax()):
            ipt = _h.GetYaxis().FindBin(pt)
            ieta = _h.GetXaxis().FindBin(abs(eta))
            SF[0] = _h.GetBinContent(ieta, ipt)
            SF_e[0] = _h.GetBinError(ieta, ipt)
        else:
            SF[0] = 1.0
            SF_e[0] = 0.0
    else:
        SF[0] = 1.0
        SF_e[0] = 0.0

# Usage example:
name = ["C", "D", "E", "F", "G", "Ds_preE", "Ds_postE", "B0_preE", "B0_postE", "Bp_preE", "Bp_postE", "DsPhiPi_preE",
        "DsPhiPi_postE"]

print("Data:")
for i in range(5):
    print("Era", name[i])
    for j in range(8):
        num = str(j)
        oldfile = ROOT.TFile.Open(
            f"/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/Analysis/2022{name[i]}_{num}_tau3mu_ReReco/AnalysedTree_data_2022{name[i]}_{num}_tau3mu_merged_ReReco.root")
        newfile = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_S{num}_tau3mu.root", "recreate")
        RM_Branch(oldfile, newfile, "tau3mu")
        oldfile.Close()
        newfile.Close()
        del oldfile
        del newfile
        f = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_S{num}_tau3mu.root", "update")
        Add_Branch(f, None, None, "Data")
        f.Close()

print("C.C.:")
for i in range(5):
    print("Era", name[i])
    for j in range(8):
        num = str(j)
        oldfile = ROOT.TFile.Open(
            f"/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/Analysis/2022{name[i]}_{num}_control_ReReco/AnalysedTree_data_control_2022{name[i]}_{num}_control_merged_ReReco.root")
        newfile = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_S{num}_control.root", "recreate")
        RM_Branch(oldfile, newfile, "control")
        oldfile.Close()
        newfile.Close()
        del oldfile
        del newfile
        f = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_S{num}_control.root", "update")
        Add_Branch(f, None, None, "Data")
        f.Close()

file = ROOT.TFile.Open(
    "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_preE.root", "read")
SF_preE = file.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")
file2 = ROOT.TFile.Open(
    "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_postE.root", "read")
SF_postE = file2.Get("NUM_GlobalMuons_PF_DEN_genTracks_abseta_pt")

file3 = ROOT.TFile.Open(
    "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/histogram_ratio.root", "read")
h_Ds_preE = file3.Get("ratio_h_Ds_preE")
h_Ds_postE = file3.Get("ratio_h_Ds_postE")
h_Bp_preE = file3.Get("ratio_h_Bp_preE")
h_Bp_postE = file3.Get("ratio_h_Bp_postE")
h_B0_preE = file3.Get("ratio_h_B0_preE")
h_B0_postE = file3.Get("ratio_h_B0_postE")
h_DsPhiPi_preE = file3.Get("ratio_h_DsPhiPi_preE")
h_DsPhiPi_postE = file3.Get("ratio_h_DsPhiPi_postE")

print("MC:")
for i in range(5, 13):
    print("Dataset", name[i])
    n = "tau3mu" if i != 12 and i != 11 else "control"
    oldfile = ROOT.TFile.Open(
        f"/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/Analysis/{name[i]}_{n}_ReReco/AnalysedTree_MC_{name[i]}_{n}_merged_ReReco.root")
    newfile = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_{n}.root", "recreate")
    if name[i] != "DsPhiPi_preE" and name[i] != "DsPhiPi_postE":
        RM_Branch(oldfile, newfile, "tau3mu")
    else:
        RM_Branch(oldfile, newfile, "control")
    oldfile.Close()
    newfile.Close()
    del oldfile
    del newfile
    f = ROOT.TFile.Open(f"New_Ntuple/Name_{name[i]}_{n}.root", "update")
    if name[i] == "Ds_preE":
        Add_Branch(f, SF_preE, h_Ds_preE, name[i])
    elif name[i] == "B0_preE":
        Add_Branch(f, SF_preE, h_B0_preE, name[i])
    elif name[i] == "Bp_preE":
        Add_Branch(f, SF_preE, h_Bp_preE, name[i])
    elif name[i] == "DsPhiPi_preE":
        Add_Branch(f, SF_preE, h_DsPhiPi_preE, name[i])

    if name[i] == "Ds_postE":
        Add_Branch(f, SF_postE, h_Ds_postE, name[i])
    elif name[i] == "B0_postE":
        Add_Branch(f, SF_postE, h_B0_postE, name[i])
    elif name[i] == "Bp_postE":
        Add_Branch(f, SF_postE, h_Bp_postE, name[i])
    elif name[i] == "DsPhiPi_postE":
        Add_Branch(f, SF_postE, h_DsPhiPi_postE, name[i])

    f.Close()
