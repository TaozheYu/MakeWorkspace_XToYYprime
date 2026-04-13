import sys,math,ctypes,array
import ROOT
import copy
import os
import matplotlib.pyplot as plt
from ROOT import gROOT, gPad, gStyle
from array import array
#from Save_tools import *

########
###This python file set the parameters 
########


Mj1 = ROOT.RooRealVar("mj1", "m_{j1}", 50., 500.)   
Mj2 = ROOT.RooRealVar("mj2", "m_{j2}", 50., 2514.)   
#Mvv = ROOT.RooRealVar("mjj", "m_{jj}", 1500,5000)  
Mvv = ROOT.RooRealVar("mjj", "m_{jj}", 1500.,5000.)  

mj1_bins = []
mj2_bins = []
mjj_bins = [] 

mj1_resolved_bins = [50, 55, 60, 66, 72, 79, 86, 94, 103, 113, 124, 136, 149, 163, 179, 196, 215, 236, 259, 284, 312, 343, 377, 414, 455, 500, 550]
mj2_resolved_bins = [50, 55, 60, 66, 72, 79, 86, 94, 103, 113, 124, 136, 149, 163, 179, 196, 215, 236, 259, 284, 312, 343, 377, 414, 455, 500, 550, 605, 665, 731, 804, 884, 972, 1069, 1175, 1292, 1421, 1563, 1719, 1890, 2079, 2286, 2514, 2765, 3041, 3345]
mjj_resolved_bins = [1452, 1597, 1756, 1931, 2124, 2336, 2569, 2825, 3107, 3417, 3758, 4133, 4546, 5000, 5500, 6050, 6655] 

mj1_boosted_bins = [50, 60, 72, 86, 103, 123, 147, 176, 211, 253, 303, 363, 435, 522] 
mj2_boosted_bins = [50, 60, 72, 86, 103, 123, 147, 176, 211, 253, 303, 363, 435, 522, 626, 751, 901, 1081, 1297]
mjj_boosted_bins = [1200, 1320, 1452, 1597, 1756, 1931, 2124, 2336, 2569, 2825, 3107, 3417, 3758, 4133, 4546, 5000, 5500, 6050, 6655]

x = ROOT.RooRealVar("x", "x", 0, 20000) 

samples = [
           #"XToYYprime_MX2000_MY120_MYprime500",  #resolved signal
           "XToYYprime_MX3000_MY200_MYprime800",  #resolved signal
           #"XToYYprime_MX4000_MY200_MYprime2000", #resolved signal
           #"XToYYprime_MX4000_MY200_MYprime600",   #boosted signal
           "QCD_madgraph_pythia8",
           #"QCD_madgraph_herwig7",
           #"QCD_herwig7_Pt",
           #"QCD_pythia8_Pt",
           "VV",
           "ST",
           "TT",
           "ZJets",
           "WJets",
           "JetHT",
          ]

bkg_samples = [
               "QCD_madgraph_pythia8",
               #"QCD_madgraph_herwig7",
               #"QCD_herwig7_Pt",
               #"QCD_pythia8_Pt",
               "VV",
               "ST",
               "TT",
               "ZJets",
               "WJets",
              ]

signal_samples = [
                  #"XToYYprime_MX2000_MY120_MYprime500",   #resolved signal  
                  "XToYYprime_MX3000_MY200_MYprime800",   #resolved signal  
                  #"XToYYprime_MX4000_MY200_MYprime2000",  #resolved signal  
                  #"XToYYprime_MX4000_MY200_MYprime600",    #boosted signal
                 ]

dataset = ["JetHT"]
samples_color = {
               "VV":ROOT.kRed+2,
               "ST":ROOT.kViolet-1,
               "TT":ROOT.kViolet,
               "ZJets":ROOT.kPink+6,
               "WJets":ROOT.kGreen,
               "QCD":ROOT.kBlue,
               "QCD_madgraph_pythia8":ROOT.kBlue,
               "QCD_madgraph_herwig7":ROOT.kBlue,
               "QCD_herwig7_Pt":ROOT.kBlue,
               "QCD_pythia8_Pt":ROOT.kBlue,
               "XToYYprime_MX4000_MY200_MYprime600":ROOT.kRed,    #boosted signal
               "XToYYprime_MX3000_MY200_MYprime800":ROOT.kRed,   #resolved signal  
               }

categories = [] 

categories_resolved = ["HP","LP","rest"] 

categories_boosted = ["HPHP","HPLP","HPrest"] 

systematics = ["nominal",
               "showerUp","showerDown",
               "MEUp","MEDown",
               "MEshowerUp","MEshowerDown",
               "JuncTotalUp","JuncTotalDown",
               "JerUp"      ,"JerDown",
               "mjetsUp"    ,"mjetsDown",
               "mjetsinvUp" ,"mjetsinvDown",
               "MErenUp"    ,"MErenDown",
               "MEfacUp"    ,"MEfacDown",
               #"PDFalphas_up","PDFalphas_down",
               "PSisrUp"    ,"PSisrDown",
               "PSfsrUp"    ,"PSfsrDown",
              ] 
systematics_names = [
                     "shower",
                     "ME",
                     "MEshower",
                     "JuncTotal",
                     "Jer",
                     "mjets",
                     "mjetsinv",
                     "MEren",
                     "MEfac",
                     #"PDFalphas",
                     "PSisr",
                     "PSfsr",
                    ] 
var_list = [Mj1,Mj2,Mvv] 

varname_list = [] 

varname_resolved_list = ["fatjet","2jets","3jets"] 

varname_boosted_list = ["leading_fatjet","subleading_fatjet","2fatjets"] 

result_resolved_dict = {
    sample: {
        category: {
            systematic: None for systematic in systematics
        } for category in categories_resolved
    } for sample in samples
}

result_boosted_dict = {
    sample: {
        category: {
            systematic: None for systematic in systematics
        } for category in categories_boosted
    } for sample in samples
}

dir_list          = {} 
hist3D_names      = {}
hist_names        = {}
hist_covert3Dto1D = {}
Roodatahist_names = {}
Roodatahist_covert3Dto1D = {}
pdf_names         = {}
pdf_covert3Dto1D  = {}


result_resolved_dict_2 = {
    sample: {
        category: {
            systematic : {
                var: None for var in varname_resolved_list
            } for systematic in systematics
        } for category in categories_resolved
    } for sample in samples
}

result_boosted_dict_2 = {
    sample: {
        category: {
            systematic : {
                var: None for var in varname_boosted_list
            } for systematic in systematics
        } for category in categories_boosted
    } for sample in samples
}

hist1D_names = {} 
pdf1D_names  = {}
Roodatahist1D_names = {} 

