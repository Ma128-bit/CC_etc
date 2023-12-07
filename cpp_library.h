#include <iostream>
#include <ROOT/RDataFrame.hxx>
#include <ROOT/RVec.hxx>
#include <ROOT/RDF/RInterface.hxx>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TLegend.h>
#include <TStyle.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TString.h>
#include <TH2F.h>

double xsection_Bp_preE = 3.508e+9, xsection_Bp_postE = 3.538e+9;
double xsection_Ds_preE = 9.827e+9, xsection_Ds_postE = 9.815e+9;
double xsection_B0_preE = 3.520e+9, xsection_B0_postE = 3.525e+9;
double xsection_DsPhiPi_preE = 1.106e+10, xsection_DsPhiPi_postE = 1.103e+10;

double lumi_tau3mu_preE = 8.052, lumi_tau3mu_postE = 26.758;
double lumi_control_preE = 0.397, lumi_control_postE = 1.33;

double BR_tau3mu = 1.0e-7, BR_control = 1.29e-5;
double BR_Dstau = 5.48e-2, BR_DsPhiPi = 1.3e-5;
double BR_Bptau = 3.33e-2, BR_B0tau = 3.35e-2;

double N_Bp_preE = 515160.0, N_Bp_postE = 1627733.0;
double N_Ds_preE = 2077873.0, N_Ds_postE = 7428463.0;
double N_B0_preE = 837468.0, N_B0_postE = 2702174.0;
double N_DsPhiPi_preE = 297926.0, N_DsPhiPi_postE = 1199059.0;

double weight_CC_preE = 0.77, weight_CC_postE = 1.03;
double weight_CC_preE_err = 0.09, weight_CC_postE_err = 0.05;

double add_weight_CC(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    if(id.Contains("_preE") && !(id.Contains("DsPhiPi"))) return weight_CC_preE;
    if(id.Contains("_postE") && !(id.Contains("DsPhiPi"))) return weight_CC_postE;
    else return 1;
}
double add_weight_CC_err(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    if(id.Contains("_preE") && !(id.Contains("DsPhiPi"))) return weight_CC_preE_err;
    if(id.Contains("_postE") && !(id.Contains("DsPhiPi"))) return weight_CC_postE_err;
    else return 1;
}
TString add_ID(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    //std::cout<<"id: "<<id.AsString()<<std::endl;
    if(id.Contains("MC_Ds_preE.root")) return "Ds_preE"; //isMC=1
    if(id.Contains("MC_Ds_postE.root")) return "Ds_postE"; //isMC=1
    if(id.Contains("MC_B0_preE.root")) return "B0_preE"; //isMC=3
    if(id.Contains("MC_B0_postE.root")) return "B0_postE"; //isMC=3
    if(id.Contains("MC_Bp_preE.root")) return "Bp_preE"; //isMC=2
    if(id.Contains("MC_Bp_postE.root")) return "Bp_postE"; //isMC=2
    if(id.Contains("MC_DsPhiPi_preE.root")) return "DsPhiPi_preE";
    if(id.Contains("MC_DsPhiPi_postE.root")) return "DsPhiPi_postE";
    if(id.Contains("Era_")) return "Data";
    else return "None";
}
double add_weight(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    if(id.Contains("MC_Ds_preE.root")) return (xsection_Ds_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Dstau/N_Ds_preE);
    if(id.Contains("MC_Ds_postE.root")) return (xsection_Ds_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Dstau/N_Ds_postE);
    if(id.Contains("MC_B0_preE.root")) return (xsection_B0_preE*lumi_tau3mu_preE*BR_tau3mu*BR_B0tau/N_B0_preE);
    if(id.Contains("MC_B0_postE.root")) return (xsection_B0_postE*lumi_tau3mu_postE*BR_tau3mu*BR_B0tau/N_B0_postE);
    if(id.Contains("MC_Bp_preE.root")) return (xsection_Bp_preE*lumi_tau3mu_preE*BR_tau3mu*BR_Bptau/N_Bp_preE);
    if(id.Contains("MC_Bp_postE.root")) return (xsection_Bp_postE*lumi_tau3mu_postE*BR_tau3mu*BR_Bptau/N_Bp_postE);
    if(id.Contains("MC_DsPhiPi_preE.root")) return (xsection_DsPhiPi_preE*lumi_control_preE*BR_control*BR_DsPhiPi/N_DsPhiPi_preE);
    if(id.Contains("MC_DsPhiPi_postE.root")) return (xsection_DsPhiPi_postE*lumi_control_postE*BR_control*BR_DsPhiPi/N_DsPhiPi_postE);
    if(id.Contains("Era_")) return 1;
    else return -1;
}
double add_weight_MC(unsigned int slot, const ROOT::RDF::RSampleInfo &id){
    if(id.Contains("MC_Ds_preE.root")) return ((N_Bp_preE/N_Ds_preE)*(BR_Dstau/BR_Bptau));
    if(id.Contains("MC_Ds_postE.root")) return ((N_Bp_postE/N_Ds_postE)*(BR_Dstau/BR_Bptau));
    if(id.Contains("MC_B0_preE.root")) return ((N_Bp_preE/N_B0_preE)*(BR_B0tau/BR_Bptau));
    if(id.Contains("MC_B0_postE.root")) return ((N_Bp_postE/N_B0_postE)*(BR_B0tau/BR_Bptau));
    if(id.Contains("MC_Bp_preE.root")) return ((N_Bp_preE/N_Bp_preE)*(BR_Bptau/BR_Bptau));
    if(id.Contains("MC_Bp_postE.root")) return ((N_Bp_postE/N_Bp_postE)*(BR_Bptau/BR_Bptau));
    if(id.Contains("Era_") || id.Contains("DsPhiPi")) return 1;
    else return -1;
}
double get_MuonSF(const TString& ID, const double pt, const double eta, TH2F* SF_pre, TH2F* SF_post){
    TH2F* SF = nullptr;
    if (ID.Contains("preE")) { SF = SF_pre;} 
    else if (ID.Contains("postE")) {SF = SF_post;}
    else if (ID.Contains("Data")) {return 1;}
    else return 1;
    int ipt = SF->GetYaxis()->FindBin(pt);
    int ieta = SF->GetXaxis()->FindBin(std::abs(eta));
    return SF->GetBinContent(ieta, ipt);
}
double get_MuonSF_err(const TString& ID, const double pt, const double eta, TH2F* SF_pre, TH2F* SF_post){
    TH2F* SF = nullptr;
    if (ID.Contains("preE")) { SF = SF_pre;} 
    else if (ID.Contains("postE")) {SF = SF_post;}
    else if (ID.Contains("Data")) {return 0;}
    else return 0;
    int ipt = SF->GetYaxis()->FindBin(pt);
    int ieta = SF->GetXaxis()->FindBin(std::abs(eta));
    return SF->GetBinError(ieta, ipt);
}
struct WeightsComputer{
    TH2F *h2D_1;
    TH2F *h2D_2;
    bool flag;
    WeightsComputer(TH2F *h1, TH2F *h2, bool f) : h2D_1(h1), h2D_2(h2), flag(f)  {}
    float operator()(const TString& ID, const double pt, const double eta) {
        if (!flag) return get_MuonSF(ID, pt, eta, h2D_1, h2D_2);
        else return get_MuonSF_err(ID, pt, eta, h2D_1, h2D_2);
    }
};
