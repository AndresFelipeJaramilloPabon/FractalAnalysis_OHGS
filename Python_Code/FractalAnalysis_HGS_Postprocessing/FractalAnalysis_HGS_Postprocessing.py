# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:59:47 2021

@author: Andrés Jaramillo
"""


import xlrd
import itertools
import matplotlib.pyplot as plt 
from matplotlib import cm
from scipy.interpolate import griddata
from scipy.stats import linregress
from scipy.stats import pearsonr
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import math
from scipy.spatial import ConvexHull
from PIL import Image
import matplotlib.patches as mpatches

# User input

# Please specify the path to the Excel spreadsheet file to be opened

loc = (r'--Specify here--')

#-------------------------------------


wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

Quant=int(sheet.cell_value(0,15))

Radius=list()
LC=list()
NO1=list()
NO2=list()
NO3=list()
NO4=list()
NO5=list()
NO6=list()
NO7=list()
NO8=list()
NO9=list()
NO10=list()

for i in range(Quant):
    Radius.append(float(sheet.cell_value(4+i,15)))
    LC.append(float(sheet.cell_value(4+i,16)))
    NO1.append(float(sheet.cell_value(4+i,17)))
    NO2.append(float(sheet.cell_value(4+i,18)))
    NO3.append(float(sheet.cell_value(4+i,19)))
    NO4.append(float(sheet.cell_value(4+i,20)))
    NO5.append(float(sheet.cell_value(4+i,21)))
    NO6.append(float(sheet.cell_value(4+i,22)))
    NO7.append(float(sheet.cell_value(4+i,23)))
    NO8.append(float(sheet.cell_value(4+i,24)))
    NO9.append(float(sheet.cell_value(4+i,25)))
    NO10.append(float(sheet.cell_value(4+i,26)))
    
labels=['Non-Optimal 1','Non-Optimal 2','Non-Optimal 3','Non-Optimal 4','Non-Optimal 5','Non-Optimal 6','Non-Optimal 7','Non-Optimal 8','Non-Optimal 9','Non-Optimal 10','Least Cost']
fig, ax = plt.subplots(dpi=600)
ax.set_xlabel('log $\epsilon$')
ax.set_ylabel('log V($\epsilon$)')
ax.set_axisbelow(True)
ax.grid()
ax.scatter(Radius,NO1,s=20,marker='x',color='black')
ax.scatter(Radius,NO2,s=20,marker='+')
ax.scatter(Radius,NO3,s=20,marker='X')
ax.scatter(Radius,NO4,s=20,marker='1')
ax.scatter(Radius,NO5,s=20,marker='3')
ax.scatter(Radius,NO6,s=20,marker='p',color='darkgreen')
ax.scatter(Radius,NO7,s=20,marker='P')
ax.scatter(Radius,NO8,s=20,marker='v',color='deeppink')
ax.scatter(Radius,NO9,s=20,marker='*',color='purple')
ax.scatter(Radius,NO10,s=20,marker='s',color='maroon')
ax.scatter(Radius,LC,s=20,color='b')
ax.legend(labels,bbox_to_anchor=(1, 1))
fig.set_size_inches(5,3.5)
plt.savefig('logVe_vs_loge.tiff', dpi=600,bbox_inches = 'tight')








