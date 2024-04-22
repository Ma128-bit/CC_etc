single_mu_SF_preE = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_preE.root"
single_mu_SF_postE = "/lustrehome/mbuonsante/Tau_3mu/CMSSW_12_4_11_patch3/src/MacroAnalysis/GM_PF_SF/SF_postE.root"
PV_SFs = "/lustrehome/mbuonsante/Tau_3mu/CC_etc/CMSSW_13_0_13/src/PV_Histo/histogram_ratio.root"

data_path = "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra"

# 2022:
tau3mu_Run2022C = data_path + "/Era_C_tau3mu.root"
tau3mu_Run2022D = data_path + "/Era_D_tau3mu.root"
tau3mu_Run2022E = data_path + "/Era_E_tau3mu.root"
tau3mu_Run2022F = data_path + "/Era_F_tau3mu.root"
tau3mu_Run2022G = data_path + "/Era_G_tau3mu.root"

control_Run2022C = data_path + "/Era_C_control.root"
control_Run2022D = data_path + "/Era_D_control.root"
control_Run2022E = data_path + "/Era_E_control.root"
control_Run2022F = data_path + "/Era_F_control.root"
control_Run2022G = data_path + "/Era_G_control.root"

MC2022_B0_pre = data_path + "/MC_B0_preE.root"
MC2022_B0_post = data_path + "/MC_B0_postE.root"
MC2022_Bp_pre = data_path + "/MC_Bp_preE.root"
MC2022_Bp_post = data_path + "/MC_Bp_postE.root"
MC2022_Ds_pre = data_path + "/MC_Ds_preE.root"
MC2022_Ds_post = data_path + "/MC_Ds_postE.root"

MC2022_DsPhiPi_pre = data_path + "/MC_DsPhiPi_preE.root"
MC2022_DsPhiPi_post = data_path + "/MC_DsPhiPi_postE.root"

# 2023:
tau3mu_Run2023B = data_path + "_2023/Era_B_tau3mu.root"
tau3mu_Run2023C = data_path + "_2023/Era_C_tau3mu.root"
tau3mu_Run2023D = data_path + "_2023/Era_D_tau3mu.root"

control_Run2023B = data_path + "_2023/Era_B_control.root"
control_Run2023C = data_path + "_2023/Era_C_control.root"
control_Run2023D = data_path + "_2023/Era_D_control.root"

MC2023_B0_pre = data_path + "_2023/MC_B0_preBPix.root"
MC2023_B0_post = data_path + "_2023/MC_B0_postBPix.root"
MC2023_Bp_pre = data_path + "_2023/MC_Bp_preBPix.root"
MC2023_Bp_post = data_path + "_2023/MC_Bp_postBPix.root"
MC2023_Ds_pre = data_path + "_2023/MC_Ds_preBPix.root"
MC2023_Ds_post = data_path + "_2023/MC_Ds_postBPix.root"

MC2023_DsPhiPi_pre = data_path + "_2023/MC_DsPhiPi_preBPix.root"
MC2023_DsPhiPi_post = data_path + "_2023/MC_DsPhiPi_postBPix.root"

data_path2 = "/lustre/cms/store/user/mbuonsan/"

tau3mu_files_MC = [
	data_path2 + "DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_preE/240202_164447",
	data_path2 + "DstoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Ds_new_Mini_postE/240202_164734",
	data_path2 + "ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_preE/240202_164318",
	data_path2 + "ButoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bu_Mini_postE/240202_164600",
	data_path2 + "BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_preE/240202_164147",
	data_path2 + "BdtoTau_Tauto3Mu_3MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimTau3mu_MCRun3_Bd_Mini_postE/240202_164027"
	
]
control_files_MC = [
	data_path2 + "DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_preE/231128_103303",
	data_path2 + "DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/SkimPhiPi_MCRun3_Mini_postE/231128_103225"	
]
tau3mu_files_2022C = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraC_stream0_Mini_v3/240204_001403",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraC_stream1_Mini_v3/240204_001426",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraC_stream2_Mini_v3/240204_001447",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraC_stream3_Mini_v3/240204_001511",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraC_stream4_Mini_v3/240204_001534",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraC_stream5_Mini_v3/240204_001555",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraC_stream6_Mini_v3/240204_001616",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraC_stream7_Mini_v3/240204_001639"
]

tau3mu_files_2022D1 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v1_stream0_Mini_v3/240204_001656",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v1_stream1_Mini_v3/240204_001715",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v1_stream2_Mini_v3/240204_001739",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v1_stream3_Mini_v3/240204_001801",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v1_stream4_Mini_v3/240204_001825",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v1_stream5_Mini_v3/240204_001844",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v1_stream6_Mini_v3/240204_001907",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v1_stream7_Mini_v3/240204_001932"
]
tau3mu_files_2022D2 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraD-v2_stream0_Mini_v3/240204_001949",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraD-v2_stream1_Mini_v3/240204_002009",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraD-v2_stream2_Mini_v3/240204_002033",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraD-v2_stream3_Mini_v3/240204_002055",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraD-v2_stream4_Mini_v3/240204_002118",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraD-v2_stream5_Mini_v3/240204_002140",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraD-v2_stream6_Mini_v3/240204_002203",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraD-v2_stream7_Mini_v3/240204_002222"
]
tau3mu_files_2022E = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraE_stream0_Mini_v3/240204_002456",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraE_stream1_Mini_v3/240204_002517",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraE_stream2_Mini_v3/240204_002543",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraE_stream3_Mini_v3/240204_002609",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraE_stream4_Mini_v3/240204_002631",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraE_stream5_Mini_v3/240204_002651",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraE_stream6_Mini_v3/240204_002715",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraE_stream7_Mini_v3/240204_002735"
]
tau3mu_files_2022F = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraF_stream0_Mini_v3/240203_234602",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraF_stream1_Mini_v3/240203_234623",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraF_stream2_Mini_v3/240203_234643",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraF_stream3_Mini_v3/240203_234705",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraF_stream4_Mini_v3/240203_234724",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraF_stream5_Mini_v3/240203_234750",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraF_stream6_Mini_v3/240203_234812",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraF_stream7_Mini_v3/240203_234834"
]

tau3mu_files_2022G = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimTau3mu_2022eraG_stream0_Mini_v3/240203_234848",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimTau3mu_2022eraG_stream1_Mini_v3/240203_234914",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimTau3mu_2022eraG_stream2_Mini_v3/240203_234941",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimTau3mu_2022eraG_stream3_Mini_v3/240203_235005",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimTau3mu_2022eraG_stream4_Mini_v3/240203_235029",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimTau3mu_2022eraG_stream5_Mini_v3/240203_235057",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimTau3mu_2022eraG_stream6_Mini_v3/240203_235124",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimTau3mu_2022eraG_stream7_Mini_v3/240203_235148"
]


control_files_2022C = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraC_stream0_Mini_v3/240204_002947",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraC_stream1_Mini_v3/240204_003014",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraC_stream2_Mini_v3/240204_003033",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraC_stream3_Mini_v3/240204_003053",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraC_stream4_Mini_v3/240204_003121",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraC_stream5_Mini_v3/240204_003141",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraC_stream6_Mini_v3/240204_003202",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraC_stream7_Mini_v3/240204_003223"
]

control_files_2022D1 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD-v1_stream0_Mini_v3/240204_003244",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD-v1_stream1_Mini_v3/240204_003307",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD-v1_stream2_Mini_v3/240204_003331",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD-v1_stream3_Mini_v3/240204_003358",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD-v1_stream4_Mini_v3/240204_003419",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD-v1_stream5_Mini_v3/240204_003441",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD-v1_stream6_Mini_v3/240204_003506",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD-v1_stream7_Mini_v3/240204_003532"
]
control_files_2022D2 = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraD-v2_stream0_Mini_v3/240204_003554",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraD-v2_stream1_Mini_v3/240204_003617",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraD-v2_stream2_Mini_v3/240204_003641",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraD-v2_stream3_Mini_v3/240204_003713",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraD-v2_stream4_Mini_v3/240204_003741",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraD-v2_stream5_Mini_v3/240204_003803",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraD-v2_stream6_Mini_v3/240204_003826",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraD-v2_stream7_Mini_v3/240204_003849"
]
control_files_2022E = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraE_stream0_Mini_v3/240204_003910",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraE_stream1_Mini_v3/240204_003934",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraE_stream2_Mini_v3/240204_003956",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraE_stream3_Mini_v3/240204_004018",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraE_stream4_Mini_v3/240204_004043",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraE_stream5_Mini_v3/240204_004110",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraE_stream6_Mini_v3/240204_004134",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraE_stream7_Mini_v3/240204_004156"
]
control_files_2022F = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraF_stream0_Mini_v3/240203_235432",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraF_stream1_Mini_v3/240203_235455",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraF_stream2_Mini_v3/240203_235519",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraF_stream3_Mini_v3/240203_235539",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraF_stream4_Mini_v3/240203_235559",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraF_stream5_Mini_v3/240203_235620",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraF_stream6_Mini_v3/240203_235643",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraF_stream7_Mini_v3/240203_235704"
]

control_files_2022G = [
	data_path2 + "ParkingDoubleMuonLowMass0/SkimDsPhiPi_2022eraG_stream0_Mini_v3/240203_235721",
	data_path2 + "ParkingDoubleMuonLowMass1/SkimDsPhiPi_2022eraG_stream1_Mini_v3/240203_235740",
	data_path2 + "ParkingDoubleMuonLowMass2/SkimDsPhiPi_2022eraG_stream2_Mini_v3/240203_235800",
	data_path2 + "ParkingDoubleMuonLowMass3/SkimDsPhiPi_2022eraG_stream3_Mini_v3/240203_235821",
	data_path2 + "ParkingDoubleMuonLowMass4/SkimDsPhiPi_2022eraG_stream4_Mini_v3/240203_235847",
	data_path2 + "ParkingDoubleMuonLowMass5/SkimDsPhiPi_2022eraG_stream5_Mini_v3/240203_235906",
	data_path2 + "ParkingDoubleMuonLowMass6/SkimDsPhiPi_2022eraG_stream6_Mini_v3/240203_235926",
	data_path2 + "ParkingDoubleMuonLowMass7/SkimDsPhiPi_2022eraG_stream7_Mini_v3/240203_235946"
]
