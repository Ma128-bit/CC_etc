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
* `SelEffNtuple.py`
  * Run as: `python3 SelEffNtuple.py`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Ntuplizer

* `SelEffAna.py`
  * Run as: `python3 SelEffAna.py`
  * Default: MC - Control channel. Pass `--tau3mu` and/or `--data`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Analysis 

* `Control.py`
  * Run as: `python3 Control.py`
  * Out: Control_Plots directory and Mass_Fits
  * Description: It is used to create Control plots and invariant mass fits
