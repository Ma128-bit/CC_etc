import sys, os, subprocess, json
from datetime import datetime
import numpy as np
import pandas as pd
import uproot
from ROOT import *
def load_data(self, file_name):
    """Load ROOT data and turn tree into a pd dataframe"""
    print("Loading data from", file_name)
    f = uproot.open(file_name)
    tree = f[self.tree_name]
    branches = self.all_branches
    data = tree.arrays(branches ,library="pd")
    return data
