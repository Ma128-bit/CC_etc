void PV_ratio_hist() {
    // Apri i file .root
    TFile *file1 = new TFile("PV_Histo/histogram_nVTx_MC.root");
    TFile *file2 = new TFile("PV_Histo/histogram_nVTx.root");

    // Leggi gli istogrammi dai file
    TH1F *h_DsPhiPi_preE = (TH1F*)file1->Get("h_MC_CC_DsPhiPi_preE");
    h_DsPhiPi_preE->Scale(1.0 / h_DsPhiPi_preE->Integral());
    
    TH1F *h_DsPhiPi_postE = (TH1F*)file1->Get("h_MC_CC_DsPhiPi_postE");
    h_DsPhiPi_postE->Scale(1.0 / h_DsPhiPi_postE->Integral());
    
    TH1F *h_B0_postE = (TH1F*)file1->Get("h_MC_B0_postE");
    h_B0_postE->Scale(1.0 / h_B0_postE->Integral());
    
    TH1F *h_B0_preE = (TH1F*)file1->Get("h_MC_B0_preE");
    h_B0_preE->Scale(1.0 / h_B0_preE->Integral());
    
    TH1F *h_Bp_postE = (TH1F*)file1->Get("h_MC_Bp_postE");
    h_Bp_postE->Scale(1.0 / h_Bp_postE->Integral());
    
    TH1F *h_Bp_preE = (TH1F*)file1->Get("h_MC_Bp_preE");
    h_Bp_preE->Scale(1.0 / h_Bp_preE->Integral());
    
    TH1F *h_Ds_preE = (TH1F*)file1->Get("h_MC_Ds_preE");
    h_Ds_preE->Scale(1.0 / h_Ds_preE->Integral());
    
    TH1F *h_Ds_postE = (TH1F*)file1->Get("h_MC_Ds_postE");
    h_Ds_postE->Scale(1.0 / h_Ds_postE->Integral());
    
    TH1F *h_C = (TH1F*)file2->Get("h_data_C");
    TH1F *h_D = (TH1F*)file2->Get("h_data_D");
    TH1F *h_E = (TH1F*)file2->Get("h_data_E");
    TH1F *h_F = (TH1F*)file2->Get("h_data_F1");
    TH1F *h_F2 = (TH1F*)file2->Get("h_data_F2");
    TH1F *h_G = (TH1F*)file2->Get("h_data_G");
    
    TH1F *h_control_C = (TH1F*)file2->Get("h_data_control_C");
    TH1F *h_control_D = (TH1F*)file2->Get("h_data_control_D");
    TH1F *h_control_E = (TH1F*)file2->Get("h_data_control_E");
    TH1F *h_control_F = (TH1F*)file2->Get("h_data_control_F1");
    TH1F *h_control_F2 = (TH1F*)file2->Get("h_data_control_F2");
    TH1F *h_control_G = (TH1F*)file2->Get("h_data_control_G");
    
    // Add gli istogrammi
    h_C->Add(h_D);
    h_C->Scale(1.0 / h_C->Integral());
    
    h_E->Add(h_F); h_E->Add(h_F2); h_E->Add(h_G);
    h_E->Scale(1.0 / h_E->Integral());
    
    h_control_C->Add(h_control_D);
    h_control_C->Scale(1.0 / h_control_C->Integral());
    
    h_control_E->Add(h_control_F); h_control_E->Add(h_control_F2); h_control_E->Add(h_control_G);
    h_control_E->Scale(1.0 / h_control_E->Integral());
    
    TCanvas *c = new TCanvas("c", "c", 1500, 800);
    c->Divide(2,1);
    c->cd(1);
    h_C->SetLineColor(kRed);
    h_C->Draw("H");
    h_E->Draw("Hsame");
    c->cd(2),
    h_control_C->SetLineColor(kRed);
    h_control_C->Draw("H");
    h_control_E->Draw("Hsame");
    
    
    // Crea un nuovo istogramma per il rapporto
    TH1F *ratio_h_Ds_preE = new TH1F("ratio_h_Ds_preE", "Ratio h_Ds_preE", 80, 0, 80);
    TH1F *ratio_h_Ds_postE = new TH1F("ratio_h_Ds_postE", "Ratio h_Ds_postE", 80, 0, 80);
    TH1F *ratio_h_Bp_preE = new TH1F("ratio_h_Bp_preE", "Ratio h_Bp_preE", 80, 0, 80);
    TH1F *ratio_h_Bp_postE = new TH1F("ratio_h_Bp_postE", "Ratio h_Bp_postE", 80, 0, 80);
    TH1F *ratio_h_B0_preE = new TH1F("ratio_h_B0_preE", "Ratio h_B0_preE", 80, 0, 80);
    TH1F *ratio_h_B0_postE = new TH1F("ratio_h_B0_postE", "Ratio h_B0_postE", 80, 0, 80);
    TH1F *ratio_h_DsPhiPi_preE = new TH1F("ratio_h_DsPhiPi_preE", "Ratio h_DsPhiPi_preE", 80, 0, 80);
    TH1F *ratio_h_DsPhiPi_postE = new TH1F("ratio_h_DsPhiPi_postE", "Ratio h_DsPhiPi_postE", 80, 0, 80);

    // Calcola il rapporto fra i due istogrammi
    ratio_h_Ds_preE->Divide(h_C, h_Ds_preE);
    ratio_h_Ds_postE->Divide(h_E, h_Ds_postE);
    ratio_h_Bp_preE->Divide(h_C, h_Bp_preE);
    ratio_h_Bp_postE->Divide(h_E, h_Bp_postE);
    ratio_h_B0_preE->Divide(h_C, h_B0_preE);
    ratio_h_B0_postE->Divide(h_E, h_B0_postE);
    ratio_h_DsPhiPi_preE->Divide(h_control_C, h_DsPhiPi_preE);
    ratio_h_DsPhiPi_postE->Divide(h_control_E, h_DsPhiPi_postE);
    
    // Crea un nuovo file .root e salva l'istogramma del rapporto
    TFile *output_file = new TFile("PV_Histo/histogram_ratio.root", "RECREATE");

    ratio_h_Ds_preE->Write();
    ratio_h_Ds_postE->Write();
    ratio_h_Bp_preE->Write();
    ratio_h_Bp_postE->Write();
    ratio_h_B0_preE->Write();
    ratio_h_B0_postE->Write();
    ratio_h_DsPhiPi_preE->Write();
    ratio_h_DsPhiPi_postE->Write();
    
    output_file->Close();
     
    // Chiudi i file .root
    file1->Close();
    file2->Close();
}
