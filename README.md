# CC_etc
Plots for CC and other things done between ntuple/analysis and xgboost

## Setting the environment

```
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv
git clone https://github.com/Ma128-bit/CC_etc/ .
scram b -j20
```

## Description of scripts
* `selections_eff.py`
  * Run as: `python3 selections_eff.py`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Ntuplizer

* `selections_eff_after_analysis.py`
  * Run as: `python3 selections_eff_after_analysis.py`
  * Default: MC - Control channel. Pass `--tau3mu` and/or `--data`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Analysis 

