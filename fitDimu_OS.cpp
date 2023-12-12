#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <RooRealVar.h>
#include <RooDataSet.h>
#include <RooDataHist.h>
#include <RooPlot.h>
#include <RooGaussian.h>
#include <RooFitResult.h>

using namespace RooFit;

void single_fit(TString cat, TString lable, TH1F* histo){
    // Crea una variabile RooRealVar per dimu_OS1
    RooRealVar x("dimu_OS1", "Dimu_OS1",  0.90, 1.10);
    int nBins = histo->GetNbinsX();
    x.setBins(nBins);

    // Crea un RooDataHist dal nostro istogramma
    RooDataHist data("data", histo->GetTitle(), RooArgSet(x), Import(*histo, kFALSE));
    
    // Crea un modello gaussiano per il fit
    RooRealVar mean("mean", "Mean", 1.0, 0.96, 1.06);
    RooRealVar sigma("sigma", "Sigma", 0.1, 0.01, 0.5);
    RooGaussian gauss("gauss", "Gaussian PDF", x, mean, sigma);

    // Crea un modello esponenziale per il fondo
    RooRealVar lambda("lambda", "Exponential Decay Parameter", -0.1, -10.0, 10.0);
    RooExponential exp("exp", "Exponential PDF", x, lambda);

    // Crea un modello composto da gaussiana e esponenziale come fondo
    RooRealVar nsig("nsig", "Number of signal events", 100, 0, 10000);
    RooRealVar nbkg("nbkg", "Number of background events", 500, 0, 10000);
    RooAddPdf model("model", "Signal + Background", RooArgList(gauss, exp), RooArgList(nsig, nbkg));

    // Effettua il fit del modello al dato
    RooFitResult *fitResult = model.fitTo(data, RooFit::Save());

    // Crea un frame per visualizzare il fit
    RooPlot *xframe = x.frame();
    model.paramOn(xframe, Parameters(RooArgSet(mean,sigma,lambda,nbkg,nsig)), Layout(0.6,0.9,0.9));
    data.plotOn(xframe);
    model.plotOn(xframe, Components(RooArgSet(gauss)), LineColor(kRed), LineStyle(kDashed));
    model.plotOn(xframe, Components(RooArgSet(exp)), LineColor(kGreen), LineStyle(kDashed) );
    model.plotOn(xframe);

    // Visualizza il frame
    TCanvas *canvas = new TCanvas("canvas", "Fit Result");
    xframe->Draw();
    canvas->SaveAs("Fit_"+lable+"_cat_"+cat+".png");
    delete canvas;
}

void fitDimu_OS() {
    TFile *file = TFile::Open("ROOTFiles/AllData.root");
    if (!file) {
        std::cerr << "Error opening file." << std::endl;
        return;
    }
    TTree *tree = dynamic_cast<TTree*>(file->Get("FinalTree"));
    if (!tree) {
        std::cerr << "Error loading the Tree." << std::endl;
        file->Close();
        return;
    }
    TH1F *h_OS1 = new TH1F("h_OS1", "Dimu_OS1 Distribution", 100, 0.96, 1.06);
    TH1F *h_OS2 = new TH1F("h_OS2", "Dimu_OS1 Distribution", 100, 0.96, 1.06);

    TString cat[3] = {"0","1","2"};
    TString OS1_2[2] = {"1","2"};

    for(int i=0; i<3;i++){
        for(int k=0; k<2;k++){
            TH1F *h_OS = new TH1F("h_OS"+OS1_2[k], "Dimu_OS Distribution", 200, 0.90, 1.10);    
            tree->Draw("dimu_OS1>>h_OS"+OS1_2[k], "isMC==0 && category=="+cat[i]);
            single_fit(cat[i], OS1_2[k] , h_OS);
            delete h_OS;
        }
    }
                
    delete file;
}
