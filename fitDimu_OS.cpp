#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <RooRealVar.h>
#include <RooDataSet.h>
#include <RooDataHist.h>
#include <RooPlot.h>
#include <RooGaussian.h>
#include <RooFitResult.h>
#include <cstdlib>

using namespace RooFit;

void Phi_fit(TString cat, TString lable, TH1F* histo){
    // Crea una variabile RooRealVar per dimu_OS1
    RooRealVar x("dimu_OS"+lable, "Dimu_OS"+lable,  0.90, 1.10);
    int nBins = histo->GetNbinsX();
    x.setBins(nBins);

    // Crea un RooDataHist dal nostro istogramma
    RooDataHist data("data", histo->GetTitle(), RooArgSet(x), Import(*histo, kFALSE));
    
    // Crea un modello gaussiano per il fit
    RooRealVar mean("mean", "Mean", 1.0, 0.96, 1.06);
    RooRealVar sigma("sigma", "Sigma", 0.02, 0.005, 0.5);
    RooGaussian gauss("gauss", "Gaussian PDF", x, mean, sigma);

    // Crea un modello esponenziale per il fondo
    RooRealVar lambda("lambda", "Exponential Decay Parameter", -0.1, -10.0, 10.0);
    RooExponential exp("exp", "Exponential PDF", x, lambda);

    // Crea un modello composto da gaussiana e esponenziale come fondo
    RooRealVar nsig("nsig", "Number of signal events", 1, 10000);
    RooRealVar nbkg("nbkg", "Number of background events", 1, 500000);
    RooAddPdf model("model", "Signal + Background", RooArgList(gauss, exp), RooArgList(nsig, nbkg));

    // Effettua il fit del modello al dato
    RooFitResult *fitResult = model.fitTo(data, RooFit::Save());

    // Crea un frame per visualizzare il fit
    RooPlot *xframe = x.frame();
    if (cat=="0") cat = "A";
    if (cat=="1") cat = "B";
    if (cat=="2") cat = "C";
    model.paramOn(xframe, Parameters(RooArgSet(sigma )), Layout(0.6,0.9,0.9));
    data.plotOn(xframe);
    model.plotOn(xframe, Components(RooArgSet(gauss)), LineColor(kRed), LineStyle(kDashed));
    model.plotOn(xframe, Components(RooArgSet(exp)), LineColor(kGreen), LineStyle(kDashed) );
    model.plotOn(xframe);

    // Visualizza il frame
    TCanvas *canvas = new TCanvas("canvas", "Fit Result");
    xframe->SetTitle("Phi -- dimu_OS"+lable+" inv. mass fit -- Cat "+cat);
    xframe->Draw();
    canvas->SaveAs("Fit/Fit_phi_dimu_OS"+lable+"_cat_"+cat+".png");
    std::cout<<"Fit_dimu_OS"+lable+"_cat_"+cat+".png  Saved!"<<std::endl;
    delete canvas;
}

void Omega_fit(TString cat, TString lable, TH1F* histo, int i){
    // Crea una variabile RooRealVar per dimu_OS1
    RooRealVar x("dimu_OS"+lable, "Dimu_OS"+lable, 0.67,0.88);
    int nBins = histo->GetNbinsX();
    x.setBins(nBins);

    // Crea un RooDataHist dal nostro istogramma
    RooDataHist data("data", histo->GetTitle(), RooArgSet(x), Import(*histo, kFALSE));
    
    // Crea un modello gaussiano per il fit
    RooRealVar mean("mean", "Mean", 0.782);
    RooRealVar sigma("sigma", "Sigma", 0.03, 0.001, 0.3);
    RooGaussian gauss("gauss", "Gaussian PDF", x, mean, sigma);

    // Crea un modello esponenziale per il fondo
    RooRealVar lambda("lambda", "Exponential Decay Parameter", -0.1, -10.0, 30.0);
    RooExponential exp("exp", "Exponential PDF", x, lambda);

    // Crea un modello composto da gaussiana e esponenziale come fondo
    int molt = 1;
    if(i==1) {molt = 2;}
    RooRealVar nsig("nsig", "Number of signal events", 1, molt*2000);
    RooRealVar nbkg("nbkg", "Number of background events", 1, molt*10000);
    RooAddPdf model("model", "Signal + Background", RooArgList(gauss, exp), RooArgList(nsig, nbkg));

    // Effettua il fit del modello al dato
    RooFitResult *fitResult = model.fitTo(data, RooFit::Save());

    // Crea un frame per visualizzare il fit
    RooPlot *xframe = x.frame();
    if (cat=="0") cat = "A";
    if (cat=="1") cat = "B";
    if (cat=="2") cat = "C";
    model.paramOn(xframe, Parameters(RooArgSet(mean,sigma)), Layout(0.6,0.9,0.9));
    data.plotOn(xframe);
    model.plotOn(xframe, Components(RooArgSet(gauss)), LineColor(kRed), LineStyle(kDashed));
    model.plotOn(xframe, Components(RooArgSet(exp)), LineColor(kGreen), LineStyle(kDashed) );
    model.plotOn(xframe);

    // Visualizza il frame
    TCanvas *canvas = new TCanvas("canvas", "Fit Result");
    xframe->SetTitle("Omega -- dimu_OS"+lable+" inv. mass fit -- Cat "+cat);
    xframe->Draw();
    canvas->SaveAs("Fit/Fit_omega_dimu_OS"+lable+"_cat_"+cat+".png");
    std::cout<<"Fit_dimu_OS"+lable+"_cat_"+cat+".png  Saved!"<<std::endl;
    delete canvas;
}

void fitDimu_OS() {
    TFile *file = TFile::Open("ROOTFiles/AllData2022.root");
    if (!file) {
        std::cerr << "Error opening file." << std::endl;
        return;
    }
    std::cerr << "Open file." << std::endl;
    TTree *tree = dynamic_cast<TTree*>(file->Get("FinalTree"));
    if (!tree) {
        std::cerr << "Error loading the Tree." << std::endl;
        file->Close();
        return;
    }
    std::cerr << "Load the Tree." << std::endl;
    TString cat[3] = {"0","1","2"};
    TString OS1_2[2] = {"1","2"};
    system("mkdir Fit");
    TCanvas *c = new TCanvas("c", "c");
    for(int i=0; i<3;i++){
        for(int k=0; k<2;k++){
            TH1F *h_OS = new TH1F("h_OS"+OS1_2[k], "Dimu_OS Distribution", 100, 0.90, 1.10);
            tree->Draw("dimu_OS"+OS1_2[k]+">>h_OS"+OS1_2[k], "(tripletMass<1.73 || tripletMass>1.83) && isMC==0 && category=="+cat[i]);
            Phi_fit(cat[i], OS1_2[k] , h_OS);
            TH1F *h_omega = new TH1F("h_omega"+OS1_2[k], "omega mass", 30, 0.67,0.88);
            tree->Draw("dimu_OS"+OS1_2[k]+">>h_omega"+OS1_2[k], "(tripletMass<1.73 || tripletMass>1.83) && isMC==0 && category=="+cat[i]);
            Omega_fit(cat[i], OS1_2[k] , h_omega, i);
            delete h_OS;
            delete h_omega;
        }
    }
    delete c;
    delete file;
}
