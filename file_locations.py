single_mu_SF_preE = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_preE.root"
single_mu_SF_postE = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_postE.root"
PV_SFs = "/lustrehome/mbuonsante/Tau_3mu/CC_etc/CMSSW_13_0_13/src/PV_Histo/histogram_ratio.root"

data_path = "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/"
    
tau3mu_Run2022C = data_path + "Era_C_tau3mu.root"
tau3mu_Run2022D = data_path + "Era_D_tau3mu.root"
tau3mu_Run2022E = data_path + "Era_E_tau3mu.root"
tau3mu_Run2022F = data_path + "Era_F_tau3mu.root"
tau3mu_Run2022G = data_path + "Era_G_tau3mu.root"

control_Run2022C = data_path + "Era_C_control.root"
control_Run2022D = data_path + "Era_D_control.root"
control_Run2022E = data_path + "Era_E_control.root"
control_Run2022F = data_path + "Era_F_control.root"
control_Run2022G = data_path + "Era_G_control.root"

MC2022_B0_pre = data_path + "MC_B0_preE.root"
MC2022_B0_post = data_path + "MC_B0_postE.root"
MC2022_Bp_pre = data_path + "MC_Bp_preE.root"
MC2022_Bp_post = data_path + "MC_Bp_postE.root"
MC2022_Ds_pre = data_path + "MC_Ds_preE.root"
MC2022_Ds_post = data_path + "MC_Ds_postE.root"

MC2022_DsPhiPi_pre = data_path + "MC_DsPhiPi_preE.root"
MC2022_DsPhiPi_post = data_path + "MC_DsPhiPi_postE.root"

data_path2 = "/lustre/cms/store/user/mbuonsan/"

tau3mu_files_MC = [
	#data_path2 + "DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_preE/231122_095004",
	#data_path2 + "DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_postE/231122_095034",
	data_path2 + "ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_preE/231122_094950",
	data_path2 + "ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_postE/231122_095020",
	#data_path2 + "BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_preE/231122_094936",
	#data_path2 + "BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_postE/231122_094920"
	
]
control_files_MC = [
	data_path2 + "DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_preE/231128_103303",
	data_path2 + "DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_postE/231128_103225"	
]
tau3mu_files_2022C = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsTau3mu_2022eraC_stream0_Mini_v3/231123_161239",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsTau3mu_2022eraC_stream1_Mini_v3/231123_161253",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsTau3mu_2022eraC_stream2_Mini_v3/231123_161307",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsTau3mu_2022eraC_stream3_Mini_v3/231123_161322",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsTau3mu_2022eraC_stream4_Mini_v3/231123_161336",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsTau3mu_2022eraC_stream5_Mini_v3/231123_161355",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsTau3mu_2022eraC_stream6_Mini_v3/231123_161413",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsTau3mu_2022eraC_stream7_Mini_v3/231123_161427"
]

tau3mu_files_2022D1 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v1_stream0_Mini_v3/231123_161758",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v1_stream1_Mini_v3/231123_161814",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v1_stream2_Mini_v3/231123_161829",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v1_stream3_Mini_v3/231123_161844",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v1_stream4_Mini_v3/231123_161859",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v1_stream5_Mini_v3/231123_161912",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v1_stream6_Mini_v3/231123_161926",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v1_stream7_Mini_v3/231123_161940"
]
tau3mu_files_2022D2 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v2_stream0_Mini_v3/231123_162031",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v2_stream1_Mini_v3/231123_162045",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v2_stream2_Mini_v3/231123_162059",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v2_stream3_Mini_v3/231123_162112",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v2_stream4_Mini_v3/231123_162126",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v2_stream5_Mini_v3/231123_162140",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v2_stream6_Mini_v3/231123_162155",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v2_stream7_Mini_v3/231123_162211"
]
tau3mu_files_2022E = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraE_stream0_Mini_v3/231123_162310",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraE_stream1_Mini_v3/231123_162325",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraE_stream2_Mini_v3/231123_162339",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraE_stream3_Mini_v3/231123_162354",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraE_stream4_Mini_v3/231123_162409",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraE_stream5_Mini_v3/231123_162424",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraE_stream6_Mini_v3/231123_162439",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraE_stream7_Mini_v3/231123_162453"
]
tau3mu_files_2022F = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraF_stream0_Mini_v3/231121_164952",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraF_stream1_Mini_v3/231121_165023",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraF_stream2_Mini_v3/231121_165056",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraF_stream3_Mini_v3/231121_165128",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraF_stream4_Mini_v3/231121_165159",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraF_stream5_Mini_v3/231121_165228",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraF_stream6_Mini_v3/231121_165258",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraF_stream7_Mini_v3/231121_165329"
]

tau3mu_files_2022G = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraG_stream0_Mini_v3/231121_164508",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraG_stream1_Mini_v3/231121_164528",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraG_stream2_Mini_v3/231121_164549",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraG_stream3_Mini_v3/231121_164609",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraG_stream4_Mini_v3/231121_164629",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraG_stream5_Mini_v3/231121_164647",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraG_stream6_Mini_v3/231121_164706",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraG_stream7_Mini_v3/231121_164725"
]


control_files_2022C = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraC_stream0_Mini_v3/231123_144112",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraC_stream1_Mini_v3/231123_144138",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraC_stream2_Mini_v3/231123_144204",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraC_stream3_Mini_v3/231123_144231",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraC_stream4_Mini_v3/231123_144258",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraC_stream5_Mini_v3/231123_144325",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraC_stream6_Mini_v3/231123_144349",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraC_stream7_Mini_v3/231123_144418"
]

control_files_2022D1 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD-v1_stream0_Mini_v3/231123_145908",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD-v1_stream1_Mini_v3/231123_150101",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD-v1_stream2_Mini_v3/231123_150153",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD-v1_stream3_Mini_v3/231123_150244",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD-v1_stream4_Mini_v3/231123_150330",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD-v1_stream5_Mini_v3/231123_150414",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD-v1_stream6_Mini_v3/231123_150457",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD-v1_stream7_Mini_v3/231123_150539"
]
control_files_2022D2 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD-v2_stream0_Mini_v3/231123_150840",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD-v2_stream1_Mini_v3/231123_150910",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD-v2_stream2_Mini_v3/231123_150942",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD-v2_stream3_Mini_v3/231123_151045",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD-v2_stream4_Mini_v3/231123_151137",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD-v2_stream5_Mini_v3/231123_151237",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD-v2_stream6_Mini_v3/231123_151331",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD-v2_stream7_Mini_v3/231123_151404"
]
control_files_2022E = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraE_stream0_Mini_v3/231123_152215",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraE_stream1_Mini_v3/231123_152229",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraE_stream2_Mini_v3/231123_152246",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraE_stream3_Mini_v3/231123_152303",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraE_stream4_Mini_v3/231123_152320",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraE_stream5_Mini_v3/231123_152335",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraE_stream6_Mini_v3/231123_152350",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraE_stream7_Mini_v3/231123_152405"
]
control_files_2022F = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraF_stream0_Mini_v3/231121_165811",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraF_stream1_Mini_v3/231121_165840",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraF_stream2_Mini_v3/231121_165909",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraF_stream3_Mini_v3/231121_165940",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraF_stream4_Mini_v3/231121_170012",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraF_stream5_Mini_v3/231121_170040",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraF_stream6_Mini_v3/231121_170110",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraF_stream7_Mini_v3/231121_170144"
]

control_files_2022G = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraG_stream0_Mini_v3/231121_170442",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraG_stream1_Mini_v3/231121_170514",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraG_stream2_Mini_v3/231121_170544",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraG_stream3_Mini_v3/231121_170615",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraG_stream4_Mini_v3/231121_170644",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraG_stream5_Mini_v3/231121_170715",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraG_stream6_Mini_v3/231121_170746",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraG_stream7_Mini_v3/231121_170816"
]
