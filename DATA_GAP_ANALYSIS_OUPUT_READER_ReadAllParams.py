# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:05:16 2020

@author: bcubrich
"""

#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:21:10 2018

@author: bcubrich
"""

import pandas as pd
import numpy as np
import seaborn as sns
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import os
#import xlrd
#import wx

#The following function is just used to get filepaths
#I usually just run it once to get the path, and then leave this 
#fucntion so that I can get othe rpaths if needed
def get_dat():
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)      #makes the dialog appear on top
    filename = askdirectory()      # Open single file
    
    return filename




#def onButton2(event):
# 
#app = wx.App()
# 
#frame = wx.Frame(None, -1, 'win.py')
#frame.SetDimensions(0,0,200,50)
# 
## Create open file dialog
#openFileDialog = wx.DirDialog(frame, "Choose folder to save output to", "",
#            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
# 
#openFileDialog.ShowModal()
#print(openFileDialog.GetPath())
#
## outfile_path is the string with the path name saved as a variable
#outfile_path = openFileDialog.GetPath()+'\\'
#openFileDialog.Destroy()
#
#del app

sites=r'U:/PLAN/BCUBRICH/Python/Parameter Reader/'\
r'PARAMETERS.xls'

sites_df=pd.read_excel(sites, converters={'SITE NAME':str,'State Code':str,
                                          'County Code':str, 'Site Code':str,
                                          'Paramter':str, 'Analyt':str, 
                                          'Method':str, 'Unit':str}) # load data
sites_df['Analyt']=sites_df['Analyt'].str.strip('()') #strip parentheses from 

directory=get_dat()

columns_raw=r'Transaction Type|Action Indicator|Assessment Type|Performing '\
        r'Agency|State Code / Tribal Indicator|County Code / Tribal Code|Site '\
        r'Number|Parameter Code|POC|Assessment Date|Assessment Number|Monitor '\
        r'Method Code|Reported Unit|Level 1 Monitor Concentration|Level 1 '\
        r'Assessment Concentration|Level 2 Monitor Concentration|Level 2 '\
        r'Assessment Concentration|Level 3 Monitor Concentration|Level 3 '\
        r'Assessment Concentration|Level 4 Monitor Concentration|Level 4 '\
        r'Assessment Concentration|Level 5 Monitor Concentration|Level 5 '\
        r'Assessment Concentration|Level 6 Monitor Concentration|Level 6 '\
        r'Assessment Concentration|Level 7 Monitor Concentration|Level 7 '\
        r'Assessment Concentration|Level 8 Monitor Concentration|Level 8 '\
        r'Assessment Concentration|Level 9 Monitor Concentration|Level 9 '\
        r'Assessment Concentration|Level 10 Monitor Concentration|Level '\
        r'10 Assessment Concentration'
        
        
print(os.listdir(directory))        
#%%        
columns=columns_raw.split('|')

text_all=''
output_df=pd.DataFrame(columns=columns)
count=0
for filename in os.listdir(directory):
    if filename.endswith(".xls") or filename.endswith(".csv"):
        with open(directory+'/'+filename) as f:
            text=f.read()
            if '11/30/2019 22.0 - 1/1/2020' not in text.split('\n')[3] and '11/29/2019 0.0 - 12/31/2019' not in text.split('\n')[3]:
                text_all+=text
#%%

final_missing_data=''

old_site=''

for line in text_all.split('\n'):
    if '1/1/2020' not in line:
        if '11/29/2019 0.0 - 12/31/2019' not in line:
            if '1st' not in line:
                if 'Last' not in line:
                    if '/' in line:
    
                        final_missing_data+=line
                        final_missing_data+='\n'
                        
                    else:
                        site = line[0:11]
                        if old_site != site:
                            old_site=site
                            final_missing_data+='\n\n'
                            final_missing_data+='---------------------------------------------'
                            final_missing_data+='\n'
                            final_missing_data+=old_site
                            final_missing_data+='\n'
                            final_missing_data+='---------------------------------------------'
                            final_missing_data+='\n'
                        final_missing_data+='--------------------------------\n'
                        final_missing_data+=line[12:20]
                        
                        if '88101-3' in line: final_missing_data += '   ****Continuous PM25*****'
                        if '88101-4' in line: final_missing_data += '   ****Continuous PM25*****'
                        if '88101-5' in line: final_missing_data += '   ****Continuous PM25*****'
                        final_missing_data+='\n'
#%%
text_file = open(directory+'/'+"summary_of_year_end_review_with_solids.txt", "wt")
n = text_file.write(final_missing_data)
text_file.close()
                        