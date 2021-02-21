# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 14:20:12 2021

@author: Andrés Jaramillo
"""

import xlrd
import itertools
import matplotlib.pyplot as plt 
from matplotlib import cm
from scipy.interpolate import griddata
from scipy.stats import linregress
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import math
from scipy.spatial import ConvexHull
from PIL import Image
import matplotlib.patches as mpatches
import statistics

# User Input

# Please specify the path to the Excel spreadsheet file to be opened

loc = (r'--Specify here--')

# Please specify diameter units in Excel spreadsheet file

# 0 - Millimeters
# 1 - Inches

u=0

#---------------------------------------------------

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

NumPipes=int(sheet.cell_value(2,22))

DiameterPipes=list()

for i in range(NumPipes):
    d=float(sheet.cell_value(i+1,16))
    if u==1:
        d=d*25.4
    DiameterPipes.append(d)

Mean=statistics.mean(DiameterPipes)
StdDev=statistics.stdev(DiameterPipes) 

f= open("Mean_StdDeviation.txt","w+")
f.write("Mean = "+str(Mean)+" mm\n")
f.write("Standard Deviation = "+str(StdDev)+" mm")
f.close() 