# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:33:17 2021

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

# User input

# Please specify the path to the Excel spreadsheet file to be opened

loc = (r'--Specify Here--')

# Please specify axis units - Cost Curve

Diameter_Units='in'

UnitCost_Units='$USD/m'

# Please specify axis units - Cost Calculation

TotalCost_Units='$USD'

#-------------------------------


wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 


Diameters=list()
UnitCosts=list()

for i in range(int(sheet.cell_value(0,0))):
    Diameters.append(float(sheet.cell_value(3+i,1)))
    UnitCosts.append(float(sheet.cell_value(3+i,2)))
    
# Power Regression
    
LND=[np.log(i) for i in Diameters]
LNU=[np.log(i) for i in UnitCosts]

m,b,r,p,std=linregress(LND,LNU)
K=np.exp(b)
n=m
CD=r**2

Y=[K*i**n for i in Diameters]

fig=plt.figure(dpi=600)
ax = fig.add_subplot()
fig.set_size_inches(3.5,3.5)
ax.scatter(Diameters,UnitCosts, c='blue',s=20, marker='o', alpha=1)
ax.plot(Diameters,Y,c='maroon',linestyle='dotted')
ax.set_xlabel('Diameter ('+Diameter_Units+')')
ax.set_ylabel('Unit Cost ('+UnitCost_Units+')')
textstr = '\n'.join((
    r'$K=%.4f$' % (K, ),
    r'$n=%.4f$' % (n, ),
    r'$R$'+chr(0x00b2)+'$=%.2f$' % (CD, )))
props = dict(boxstyle='round', facecolor='None', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
ax.set_yticklabels(['${:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
plt.savefig('CostCurve.tiff', dpi=600,bbox_inches = 'tight')

Costs=list()

for j in range(11):
    PartialCost=list()
    for i in range(int(sheet.cell_value(0,1))):
        PartialCost.append(round(K,4)*float(sheet.cell_value(6+i,18))*float(sheet.cell_value(6+i,19+j))**round(n,4))
    Costs.append(sum(PartialCost))

f= open("CostCalculation.txt","w+")
f.write("Optimal Design Cost = $ "+'%.0f' % (Costs[0], )+'\n')
f.write("Non-Optimal Design 1 Cost = $ "+'%.0f' % (Costs[1], )+'\n')
f.write("Non-Optimal Design 2 Cost = $ "+'%.0f' % (Costs[2], )+'\n')
f.write("Non-Optimal Design 3 Cost = $ "+'%.0f' % (Costs[3], )+'\n')
f.write("Non-Optimal Design 4 Cost = $ "+'%.0f' % (Costs[4], )+'\n')
f.write("Non-Optimal Design 5 Cost = $ "+'%.0f' % (Costs[5], )+'\n')
f.write("Non-Optimal Design 6 Cost = $ "+'%.0f' % (Costs[6], )+'\n')
f.write("Non-Optimal Design 7 Cost = $ "+'%.0f' % (Costs[7], )+'\n')
f.write("Non-Optimal Design 8 Cost = $ "+'%.0f' % (Costs[8], )+'\n')
f.write("Non-Optimal Design 9 Cost = $ "+'%.0f' % (Costs[9], )+'\n')
f.write("Non-Optimal Design 10 Cost = $ "+'%.0f' % (Costs[10], )+'\n')

     
f.close()     
