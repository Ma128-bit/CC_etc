#include "RooRealVar.h"
#include "RooStats/SPlot.h"
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooExponential.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooAddition.h"
#include "RooProduct.h"
#include "RooAbsPdf.h"
#include "RooFitResult.h"
#include "RooWorkspace.h"
#include "RooConstVar.h"
    
#include "TFile.h"
    
#include "TCanvas.h"
#include "TLegend.h"

#include <iomanip>

using namespace RooFit;
using namespace RooStats;

void AddModel(RooWorkspace &ws){
    RooRealVar tripletMass("tripletMass", "M_{inv}", 1.65, 2.05, "GeV");
    std::cout << "make Ds model" << std::endl;
    RooRealVar mDs("mDs", "Ds Mass", 1.968, 1.95, 1.98, "GeV");
    RooRealVar sigmaDs("sigmaDs", "Width of Ds Gaussian", 0.012, 0.0001, 0.4, "GeV");
    RooGaussian mDsModel("mDsModel", "Ds Model", tripletMass, mDs, sigmaDs);

    std::cout << "make Dp model" << std::endl;
    RooRealVar mDp("mDp", "Dp Mass", 1.869, 1.85, 1.88, "GeV");
    RooRealVar sigmaDp("sigmaDp", "Width of Dp Gaussian", 0.015, 0.0001, 0.4, "GeV");
    RooGaussian mDpModel("mDpModel", "Dp Model", tripletMass, mDp, sigmaDp);

    std::cout << "make bkg model" << std::endl;
    RooRealVar lambda("lambda", "lambda of Exponential", -1.44, -10, 10);
    RooExponential bkgModel("bkgModel", "Exponential", tripletMass, lambda);

    // --------------------------------------
    // combined model
    RooRealVar nsigDs("nsigDs", "fitted yield for Ds", 12000, 0., 20000);
    RooRealVar nsigDp("nsigDp", "fitted yield for Dp", 3100, 0., 20000);
    RooRealVar nbkg("nbkg", "fitted yield for bkg", 154000, 0., 1800000);

    // now make the combined models
    std::cout << "make full model" << std::endl;
    RooAddPdf massModel("massModel", "invariant mass model", RooArgList(mDsModel, mDpModel, bkgModel), RooArgList(nsigDs, nsigDp, nbkg));
    
    std::cout << "import model" << std::endl;

    ws.import(massModel, RecycleConflictNodes());
}

void AddMC_Model(RooWorkspace &ws){
    RooRealVar tripletMass("tripletMass", "M_{inv}", 1.65, 2.05, "GeV");
    std::cout << "make Ds model" << std::endl;
    RooRealVar mDs("mDs", "Ds Mass", 1.968, 1.95, 1.98, "GeV");
    RooRealVar sigmaDs("sigmaDs", "Width of Ds Gaussian", 0.012, 0.0001, 0.4, "GeV");
    RooGaussian mDsModel("mDsModel", "Ds Model", tripletMass, mDs, sigmaDs);

    std::cout << "make bkg model" << std::endl;
    RooRealVar lambda("lambda", "lambda of Exponential", -1.44, -10, 10);
    RooExponential bkgModel("bkgModel", "Exponential", tripletMass, lambda);

    // --------------------------------------
    // combined model
    RooRealVar nsigDs("nsigDs", "fitted yield for Ds", 100000, 0., 1800000);
    RooRealVar nbkg("nbkg", "fitted yield for bkg", 2000, 0., 20000);

    // now make the combined models
    std::cout << "make full model" << std::endl;
    RooAddPdf massModel("massModel", "invariant mass model", RooArgList(mDsModel, bkgModel), RooArgList(nsigDs, nbkg));
    
    std::cout << "import model" << std::endl;

    ws.import(massModel, RecycleConflictNodes());
}
void AddData(RooWorkspace &ws, TString name_file = "AllControl2022.root", TString tree_name = "FinalTree", TString selMC = "isMC==0"){
    TFile *file = new TFile("ROOTFiles/"+name_file);
    TTree *tree = (TTree*)file->Get(tree_name);
    RooAbsPdf *model = ws.pdf("model");
    RooRealVar *tripletMass = ws.var("tripletMass");
    RooArgSet variables;
    for (const auto& branch : *tree->GetListOfBranches()) {
        TString branchName = branch->GetName();
        if (!branchName.Contains("__") && branchName!="tripletMass") { // Assicurati di non includere le variabili aggiuntive (es: numero di eventi)
            RooRealVar* var = new RooRealVar(branchName.Data(), branchName.Data(), -9999999999999999999999999999., 9999999999999999999999999999.);
            variables.add(*var);
        }
    }
    variables.add(*tripletMass);
    //TString selez = selMC + " && (Ptmu3 > 1.2 && ((Ptmu1>3.5 && Etamu1<1.2) || (Ptmu1>2.0 && Etamu1>=1.2 && Etamu1<=2.4)) && ((Ptmu2>3.5 && Etamu2<1.2) || (Ptmu2>2.0 && Etamu2>=1.2 && Etamu2<=2.4)))";
    TString selez = selMC;
    RooDataSet dataset("dataset", "dataset", variables, Import(*tree),Cut(selez), WeightVar("control_weight"));

    ws.import(dataset, Rename("data"));
}

void DoSPlot(RooWorkspace &ws){
    std::cout << "Calculate sWeights" << std::endl;

    // get what we need out of the workspace to do the fit
    RooAbsPdf *massModel = ws.pdf("massModel");
    RooRealVar *nsigDs = ws.var("nsigDs");
    RooRealVar *nsigDp = ws.var("nsigDp");
    RooRealVar *nbkg = ws.var("nbkg");
    RooDataSet& data = static_cast<RooDataSet&>(*ws.data("data"));

    RooMsgService::instance().setSilentMode(true);

    std::cout << "\n\n------------------------------------------\nThe dataset before creating sWeights:\n";
    data.Print();

    RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR);

    RooStats::SPlot sData{"sData", "An SPlot", data, massModel, RooArgList(*nsigDs, *nsigDp, *nbkg)};

    std::cout << "\n\nThe dataset after creating sWeights:\n";
    data.Print();

    // Check that our weights have the desired properties

    std::cout << "\n\n------------------------------------------\n\nCheck SWeights:" << std::endl;

    std::cout << std::endl << "Yield of Ds is\t" << nsigDs->getVal() << ".  From sWeights it is " << sData.GetYieldFromSWeight("nsigDs") << std::endl;
    
    std::cout << "Yield of Dp is\t" << nsigDp->getVal() << ".  From sWeights it is " << sData.GetYieldFromSWeight("nsigDp") << std::endl << std::endl;

    std::cout << "Yield of bkg is\t" << nbkg->getVal() << ".  From sWeights it is " << sData.GetYieldFromSWeight("nbkg") << std::endl << std::endl;

    for (Int_t i = 0; i < 10; i++) {
        std::cout << "Ds Weight for event " << i << std::right << std::setw(12) << sData.GetSWeight(i, "nsigDs") << "  Dp Weight"
                << std::setw(12) << sData.GetSWeight(i, "nsigDp") << "  Total Weight" << std::setw(12) << sData.GetSumOfEventSWeight(i)
                << std::endl;
    }

    std::cout << std::endl;

    // import this new dataset with sWeights
    std::cout << "import new dataset with sWeights" << std::endl;
    ws.import(data, Rename("dataWithSWeights"));

    RooMsgService::instance().setGlobalKillBelow(RooFit::INFO);
}

void DoSPlotMC(RooWorkspace &ws){
    std::cout << "Calculate sWeights" << std::endl;

    // get what we need out of the workspace to do the fit
    RooAbsPdf *massModel = ws.pdf("massModel");
    RooRealVar *nsigDs = ws.var("nsigDs");
    RooRealVar *nbkg = ws.var("nbkg");
    RooDataSet& data = static_cast<RooDataSet&>(*ws.data("data"));

    RooMsgService::instance().setSilentMode(true);

    std::cout << "\n\n------------------------------------------\nThe dataset before creating sWeights:\n";
    data.Print();

    RooMsgService::instance().setGlobalKillBelow(RooFit::ERROR);

    RooStats::SPlot sData{"sData", "An SPlot", data, massModel, RooArgList(*nsigDs, *nbkg)};

    std::cout << "\n\nThe dataset after creating sWeights:\n";
    data.Print();

    // Check that our weights have the desired properties

    std::cout << "\n\n------------------------------------------\n\nCheck SWeights:" << std::endl;

    std::cout << std::endl << "Yield of Ds is\t" << nsigDs->getVal() << ".  From sWeights it is " << sData.GetYieldFromSWeight("nsigDs") << std::endl;
    
    std::cout << "Yield of bkg is\t" << nbkg->getVal() << ".  From sWeights it is " << sData.GetYieldFromSWeight("nbkg") << std::endl << std::endl;

    for (Int_t i = 0; i < 10; i++) {
        std::cout << "Ds Weight for event " << i << std::right << std::setw(12) << sData.GetSWeight(i, "nsigDs") << "  nbkg Weight"
                << std::setw(12) << sData.GetSWeight(i, "nbkg") << "  Total Weight" << std::setw(12) << sData.GetSumOfEventSWeight(i)
                << std::endl;
    }

    std::cout << std::endl;

    // import this new dataset with sWeights
    std::cout << "import new dataset with sWeights" << std::endl;
    ws.import(data, Rename("dataWithSWeights"));

    RooMsgService::instance().setGlobalKillBelow(RooFit::INFO);
}

void MakePlots(RooWorkspace &ws)
{
    std::cout << "make plots" << std::endl;

    TCanvas *cdata = new TCanvas("sPlot", "sPlot demo");
    cdata->Divide(1, 3);
    
    RooRealVar *tripletMass = ws.var("tripletMass");
    auto& data = static_cast<RooDataSet&>(*ws.data("dataWithSWeights"));

    // create weighted data sets
    RooDataSet dataDs_w{data.GetName(), data.GetTitle(), &data, *data.get(), nullptr, "nsigDs_sw"};
    RooDataSet dataDp_w{data.GetName(), data.GetTitle(), &data, *data.get(), nullptr, "nsigDp_sw"};
    RooDataSet databkg{data.GetName(), data.GetTitle(), &data, *data.get(), nullptr, "nbkg_sw"};

    cdata->cd(1);
    RooPlot *frame = tripletMass->frame(Title("Invaraint Mass after sPlot"));
    dataDs_w.plotOn(frame, DataError(RooAbsData::SumW2));
    frame->Draw();
    
    cdata->cd(2);
    RooPlot *frame2 = tripletMass->frame(Title("Invaraint Mass after sPlot"));
    dataDp_w.plotOn(frame2, DataError(RooAbsData::SumW2));
    frame2->Draw();

    cdata->cd(3);
    RooPlot *frame3 = tripletMass->frame(Title("Invaraint Mass after sPlot"));
    databkg.plotOn(frame3, DataError(RooAbsData::SumW2));
    frame3->Draw();

    cdata->Draw();
    //cdata->SaveAs("SPlot.gif");
}

void DsPhiPi_sPlot(TString name_file = "AllControl2022", TString tree_name = "FinalTree", int isMC = 0){
    RooWorkspace wspace{"myWS"};
    TString selMC ="";
    if(isMC == 0) selMC = selMC + Form("isMC==%d", isMC); 
    else selMC = selMC + "isMC>0";
    std::cout<<selMC<<std::endl;
    if(isMC == 0) AddModel(wspace);
    else AddMC_Model(wspace);
    AddData(wspace, name_file+".root", tree_name, selMC);
    if(isMC == 0) DoSPlot(wspace);
    else DoSPlotMC(wspace);
    const TTree *tree = wspace.data("dataWithSWeights")->GetClonedTree();

    std::vector<std::string>  branchNames;
    TFile *file = new TFile(name_file+"_sPlot_MC_"+Form("%d", isMC)+".root", "RECREATE");
    tree->Write(tree_name, TObject::kOverwrite);
    for (const auto& branch : *const_cast<TTree*>(tree)->GetListOfBranches()) {
        std::string branchName = branch->GetName();
        if (branchName!="nsigDp_sw" && branchName!="L_nsigDs") {
            branchNames.push_back(branchName);
        }
    }
    file->Close();
    ROOT::EnableImplicitMT(); // Tell ROOT you want to go parallel
    ROOT::RDataFrame d(tree_name, name_file+"_sPlot_MC_"+Form("%d", isMC)+".root"); 
    d.Snapshot(tree_name, name_file+"_sPlot_MC_"+Form("%d", isMC)+"_v2.root", branchNames);
}
