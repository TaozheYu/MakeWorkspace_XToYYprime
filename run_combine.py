import sys,math,ctypes,array
import ROOT
import os
import copy
import re
import matplotlib.pyplot as plt
from ROOT import gROOT, gPad, gStyle
from array import array
#from Save_tools import *
from parameter import *
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-y', '--years', dest='years', action='store', type=str, choices=['2016', '2016APV', '2017', '2018'], default='2017')
parser.add_argument('-t', '--topology', dest='topology', action='store', type=str, choices=['boosted', 'resolved'], default='resolved')
parser.add_argument('-rt', '--runtype', dest='runtype', action='store', type=str, choices=['limit', 'fit'], default='limit')


args = parser.parse_args()
year = args.years
topology = args.topology
runtype = args.runtype

path_fw = os.environ['CMSSW_BASE']+"/src/MakeWorkspace_XToYYprime/"
store_path = path_fw +"/"+ year + "_" + topology

# for different topology, we use the different bins
if topology == "resolved":
  mj1_bins = mj1_resolved_bins.copy() 
  mj2_bins = mj2_resolved_bins.copy() 
  mjj_bins = mjj_resolved_bins.copy() 

  categories = categories_resolved.copy()

  varname_list = varname_resolved_list.copy()

  dir_list          = copy.deepcopy(result_resolved_dict)
  hist3D_names      = copy.deepcopy(result_resolved_dict)
  hist_names        = copy.deepcopy(result_resolved_dict)
  hist_covert3Dto1D = copy.deepcopy(result_resolved_dict)
  Roodatahist_names = copy.deepcopy(result_resolved_dict)
  Roodatahist_covert3Dto1D = copy.deepcopy(result_resolved_dict)
  pdf_names         = copy.deepcopy(result_resolved_dict)
  pdf_covert3Dto1D  = copy.deepcopy(result_resolved_dict)

  hist1D_names = copy.deepcopy(result_resolved_dict_2)
  pdf1D_names = copy.deepcopy(result_resolved_dict_2)
  Roodatahist1D_names = copy.deepcopy(result_resolved_dict_2)

if topology == "boosted":
  mj1_bins = mj1_boosted_bins.copy() 
  mj2_bins = mj2_boosted_bins.copy() 
  mjj_bins = mjj_boosted_bins.copy() 

  categories = categories_boosted.copy()

  varname_list = varname_boosted_list.copy()

  dir_list          = copy.deepcopy(result_boosted_dict)
  hist3D_names      = copy.deepcopy(result_boosted_dict)
  hist_names        = copy.deepcopy(result_boosted_dict)
  hist_covert3Dto1D = copy.deepcopy(result_boosted_dict)
  Roodatahist_names = copy.deepcopy(result_boosted_dict)
  Roodatahist_covert3Dto1D = copy.deepcopy(result_boosted_dict)
  pdf_names         = copy.deepcopy(result_boosted_dict)
  pdf_covert3Dto1D  = copy.deepcopy(result_boosted_dict)

  hist1D_names = copy.deepcopy(result_boosted_dict_2)
  pdf1D_names = copy.deepcopy(result_boosted_dict_2)
  Roodatahist1D_names = copy.deepcopy(result_boosted_dict_2)

def main():
  os.chdir(store_path)
  mass_points = [re.search(r'MX\d+', s).group() for s in signal_samples]
  for i, mass_point in enumerate(mass_points): 
    os.chdir(store_path+"/"+signal_samples[i])
    if runtype == "limit":
      os.system(f"combineCards.py HP=datacard_{categories[0]}_{mass_point}.txt LP=datacard_{categories[1]}_{mass_point}.txt > datacard_SR_{mass_point}.txt")
      os.system(f"text2workspace.py datacard_SR_{mass_point}.txt -o workspace_SR_{mass_point}.root")
      os.system(f"combine -M AsymptoticLimits workspace_SR_{mass_point}.root -t -1 > combine_result_{mass_point}.txt")
      os.system(f"cat combine_result_{mass_point}.txt")
    if runtype == "fit":
      print(f"start to run the {signal_samples[i]} FitDiagnostics" )
      os.system(f"text2workspace.py datacard_rest_{mass_point}.txt -o workspace_CR.root")
      os.system("combine -M FitDiagnostics workspace_CR.root --saveShapes --saveWithUncertainties --cminDefaultMinimizerStrategy 0 --ignoreCovWarning -n postfit ")
  
if __name__ == "__main__":
  main()
