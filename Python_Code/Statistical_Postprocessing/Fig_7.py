# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:44:19 2021

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

labels1=['Two Reservoirs','Pescara','Andalucía Alta','Carmen del Viboral']
labels2=['LC','NO1','NO2','NO3','NO4','NO5','NO6','NO7','NO8','NO9','NO10']

MeanTR=[170.00,176.00,179.00,182.00,188.00,194.00,194.00,197.00,209.00,257.00,329.00]
MeanPescara=[166.67,168.43,178.79,242.93,290.91,391.67,368.43,377.78,385.10,386.62,480.81]
MeanAndalucia=[76.27,77.19,78.74,91.16,96.59,97.37,103.43,110.07,111.76,116.28,393.84]
MeanCarmen=[81.26,82.56,103.59,109.02,120.75,134.98,141.97,207.29,203.31,242.35,299.46]

StdTR=[43.95,44.60,44.60,47.91,50.24,51.74,51.74,56.68,56.68,96.21,106.85]
StdPescara=[102.08,95.34,117.77,163.27,186.31,204.13,193.27,184.71,203.51,208.26,250.48]
StdAndalucia=[1.34,4.92,7.63,29.28,33.24,33.70,36.32,37.92,38.07,38.76,235.21]
StdCarmen=[18.94,21.03,38.68,40.86,59.74,93.04,109.03,189.10,180.53,209.84,221.84]

fig, (ax1,ax2) = plt.subplots(1,2,dpi=600)
fig.set_size_inches(12,4)
ax1.plot(labels2,MeanTR,marker='o',linestyle='dotted')
ax1.plot(labels2,MeanPescara,linestyle='dotted',marker='X')
ax1.plot(labels2,MeanAndalucia,linestyle='dotted',marker='*')
ax1.plot(labels2,MeanCarmen,linestyle='dotted', marker='p')
ax1.set_title('Mean')
ax1.set_ylabel('$\mu$ (mm)')

ax2.plot(labels2,StdTR,marker='o',linestyle='dotted')
ax2.plot(labels2,StdPescara,linestyle='dotted',marker='X')
ax2.plot(labels2,StdAndalucia,linestyle='dotted',marker='*')
ax2.plot(labels2,StdCarmen,linestyle='dotted',marker='p')
ax2.legend(labels1,bbox_to_anchor=(1, 0.7))
ax2.set_title('Standard Deviation')
ax2.set_ylabel('$\sigma$ (mm)')

plt.tight_layout()
plt.savefig('Fig_7.tiff', dpi=600,bbox_inches = 'tight')