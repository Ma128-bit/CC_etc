#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <RooRealVar.h>
#include <RooDataSet.h>
#include <RooDataHist.h>
#include <RooPlot.h>
#include <RooGaussian.h>
#include <RooFitResult.h>

void single_fit(TString cat, TString lable, TH1F* histo){
    // Crea una variabile RooRealVar per dimu_OS1
    RooRealVar x("dimu_OS1", "Dimu_OS1", 0.96, 1.06);

    // Crea un RooDataHist dal nostro istogramma
    RooDataHist data("data", "Data from Tree", x, RooFit::Import(*histo));

    // Crea un modello gaussiano per il fit
    RooRealVar mean("mean", "Mean", 1.0, 0.96, 1.06);
    RooRealVar sigma("sigma", "Sigma", 0.01, 0.001, 0.1);
    RooGaussian gauss("gauss", "Gaussian PDF", x, mean, sigma);

    // Crea un modello esponenziale per il fondo
    RooRealVar lambda("lambda", "Exponential Decay Parameter", -0.1, -1.0, 0.0);
    RooExponential exp("exp", "Exponential PDF", x, lambda);

    // Crea un modello composto da gaussiana e esponenziale come fondo
    RooRealVar nsig("nsig", "Number of signal events", 100, 0, 10000);
    RooRealVar nbkg("nbkg", "Number of background events", 500, 0, 10000);
    RooAddPdf model("model", "Signal + Background", RooArgList(gauss, exp), RooArgList(nsig, nbkg));

    // Effettua il fit del modello al dato
    RooFitResult *fitResult = model.fitTo(data, RooFit::Save());

    // Crea un frame per visualizzare il fit
    RooPlot *frame = x.frame();
    data.plotOn(frame);
    gauss.plotOn(frame);

    // Visualizza il frame
    TCanvas *canvas = new TCanvas("canvas", "Fit Result");
    frame->Draw();
    canvas->SaveAs("Fit_"+lable+"_cat_"+cat+".png");
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

    tree->Draw("dimu_OS1>>h_OS1", "isMC==0 && category==0");
    tree->Draw("dimu_OS1>>h_OS2", "isMC==0 && category==0");


    single_fit(TH1F* h_OS1);
    

    // Pulisci la memoria
    delete histogram;
    delete file;
    delete canvas;
}
