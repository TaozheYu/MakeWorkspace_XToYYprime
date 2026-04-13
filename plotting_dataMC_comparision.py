import sys,math,ctypes,array
import ROOT
import os
import matplotlib.pyplot as plt
from ROOT import gROOT, gPad, gStyle
from array import array
from Save_tools import *
from parameter import *
from argparse import ArgumentParser

ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetFrameBorderMode(0)
ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetPalette(1,0,1.)
ROOT.gStyle.SetTitleX(0.5) #title X location
ROOT.gStyle.SetTitleY(0.96) #title Y location
ROOT.gStyle.SetPaintTextFormat(".2f")

parser = ArgumentParser()
parser.add_argument('-y', '--years', dest='years', action='store', type=str, choices=['2016', '2016APV', '2017', '2018'], default='2018')
parser.add_argument('-t', '--topology', dest='topology', action='store', type=str, choices=['boosted', 'resolved'], default='resolved')
parser.add_argument('-i', '--inputpath', dest='inputpath', action='store', type=str, default='/data/dust/group/cms/searches-desy/diboson/diboson_output_2018/debug_test/hists/')

args = parser.parse_args()
year = args.years
topology = args.topology
inputpath = args.inputpath

Cuts = ["Cut 008 HT_cut"]
Variables = ["DeltaEta_YYprime"]

path_fw = os.environ['CMSSW_BASE']+"/src/MakeWorkspace_XToYYprime/"
store_path = path_fw +"/"+ year + "_" + topology


if topology == "resolved":

  categories = categories_resolved.copy()

  varname_list = varname_resolved_list.copy()

  dir_list          = copy.deepcopy(result_resolved_dict)
  hist3D_names      = copy.deepcopy(result_resolved_dict)
  hist_names        = copy.deepcopy(result_resolved_dict)

if topology == "boosted":
  categories = categories_boosted.copy()

  varname_list = varname_boosted_list.copy()

  dir_list          = copy.deepcopy(result_boosted_dict)
  hist3D_names      = copy.deepcopy(result_boosted_dict)
  hist_names        = copy.deepcopy(result_boosted_dict)


if __name__ == "__main__":

 for i, Cut in enumerate(Cuts):
  for Variable in Variables:

   os.chdir(path_fw)
   CreatDirectory(store_path)
   os.chdir(store_path)
   
   openFile = inputpath + Cut + "_" + Variable + ".root" 

   file = ROOT.TFile(openFile)

   for sample in samples:
     for category in categories: 
       for systematic in systematics:
         print (sample)
         dir_list[sample][category][systematic]=[]                    
         # signal sample don't have PDF systematics
         '''
         if sample == "XToYYprime_MX3000" and systematic == "PDFalphas_up":
            continue
         if sample == "XToYYprime_MX3000" and systematic == "PDFalphas_down":
            continue
         # data don't have systematics
         if sample == "JetHT" and systematic != "nominal":
            continue
         '''
         #Read the directories
         #Read_Hist_Directory(file,sample,systematic,category,dir_list[sample][category][systematic])
         if sample in ["VV"]: 
            Read_Hist_Directory_nosys(file,"ZZ",systematic,category,dir_list[sample][category][systematic])
            Read_Hist_Directory_nosys(file,"WZ",systematic,category,dir_list[sample][category][systematic])
            Read_Hist_Directory_nosys(file,"WW",systematic,category,dir_list[sample][category][systematic])
         Read_Hist_Directory_nosys(file,sample,systematic,category,dir_list[sample][category][systematic])
         #Read TT, QCD background and signal hist in direstories
         if dir_list[sample][category][systematic]==[]:
           continue
         hist_names[sample][category][systematic] = Read_1DHist(dir_list[sample][category][systematic],sample)
         ####QCD madgraph+hewig7 cross section have problem, so I normlize it to madgraph+pythia8
         if sample == "QCD_madgraph_herwig7":
           hist_names[sample][category][systematic].Scale(1504.84)
         if sample == "QCD_herwig7_Pt":
           hist_names[sample][category][systematic].Scale(1.3478)
         if sample == "QCD_pythia8_Pt":
           hist_names[sample][category][systematic].Scale(1.)

   #plot_prefit(store_path,Cut,Variable,bkg_samples,signal_samples,samples_color,categories,varname_list,hist_names)
   plot_MC(store_path,Cut,Variable,year,bkg_samples,signal_samples,samples_color,categories,varname_list,hist_names)

   #Make pesudo data
   for category in categories: 
     for sample in samples:
       print (sample+" "+category+ " yield is ",  hist_names[sample][category]["nominal"].Integral()) 
   print (Variable + " done !")
   
