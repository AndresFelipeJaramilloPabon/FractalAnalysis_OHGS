# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 13:56:43 2020

@author: Andrés Jaramillo
"""
# Andrés Felipe Jaramillo Pabón - 201713473

# Libraries

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

# Please specify the path to Cazuca Optimal Design Excel spreadsheet file

loc = (r'--Specify here--') 

# Please specify the path to Cazuca Non-Optimal 10 Design Excel spreadsheet file  

loc1 = (r'--Specify here--') 

#-------------------------------------------------------

# 1. Reading data

# Please specify the path to the Excel spreadsheet file to be opened

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

# 2. Data Storage
NumNodes=int(sheet.cell_value(0,22))
NumReservoirs=int(sheet.cell_value(1,22))
NumPipes=int(sheet.cell_value(2,22))
Pmin=sheet.cell_value(3,22)

Nodes=list()

for i in range(NumNodes):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,0)
    Var['X']=sheet.cell_value(i+1,1)
    Var['Y']=sheet.cell_value(i+1,2)
    Var['Z']=sheet.cell_value(i+1,3)
    Var['Q']=sheet.cell_value(i+1,4)
    Var['HGL']=sheet.cell_value(i+1,5)
    Nodes.append(Var)

Reservoirs=list()

for i in range(NumReservoirs):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,7)
    Var['X']=sheet.cell_value(i+1,8)
    Var['Y']=sheet.cell_value(i+1,9)
    Var['Z']=sheet.cell_value(i+1,10)
    Var['HGL']=sheet.cell_value(i+1,11)
    Reservoirs.append(Var)

Pipes=list()

for i in range(NumPipes):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,13)
    Var['NI']=sheet.cell_value(i+1,14)
    Var['NF']=sheet.cell_value(i+1,15)
    Var['D']=sheet.cell_value(i+1,16)
    Var['L']=sheet.cell_value(i+1,17)
    Var['km']=sheet.cell_value(i+1,18)
    Var['Q']=sheet.cell_value(i+1,19)
    Pipes.append(Var)

# 2. Network Tracing
    
NodesX=list()
NodesY=list()
NodesZ=list()

for i in range(len(Reservoirs)):
    NodesX.append(Reservoirs[i]['X'])
    NodesY.append(Reservoirs[i]['Y'])
    NodesZ.append(Reservoirs[i]['Z'])
    
for i in range(len(Nodes)):
    NodesX.append(Nodes[i]['X'])
    NodesY.append(Nodes[i]['Y'])
    NodesZ.append(Nodes[i]['Z'])
    
fig = plt.figure()
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax1 = fig.add_subplot(1, 2, 2, projection='3d')
fig.set_size_inches(15, 8)
ax.scatter(NodesX, NodesY, NodesZ, c='black', marker='o', alpha=1)
ax1.scatter(NodesX, NodesY, NodesZ, c='black', marker='o', alpha=1)

for i in range(len(Pipes)):
    NI=Pipes[i]['NI']
    NF=Pipes[i]['NF']
    X=list()
    Y=list()
    Z=list()
    v=None
    for i in range(len(Reservoirs)):
        v=Reservoirs[i]['ID']
        if v==NI:
            X.append(Reservoirs[i]['X'])
            Y.append(Reservoirs[i]['Y'])
            Z.append(Reservoirs[i]['Z'])
            break
    for i in range(len(Nodes)):
        v=Nodes[i]['ID']
        if v==NI:
            X.append(Nodes[i]['X'])
            Y.append(Nodes[i]['Y'])
            Z.append(Nodes[i]['Z'])
            break
    for i in range(len(Reservoirs)):
        v=Reservoirs[i]['ID']
        if v==NF:
            X.append(Reservoirs[i]['X'])
            Y.append(Reservoirs[i]['Y'])
            Z.append(Reservoirs[i]['Z'])
            break
    for i in range(len(Nodes)):
        v=Nodes[i]['ID']
        if v==NF:
            X.append(Nodes[i]['X'])
            Y.append(Nodes[i]['Y'])
            Z.append(Nodes[i]['Z'])
            break
    ax.plot(X,Y,Z,color='darkblue') 
    ax1.plot(X,Y,Z,color='darkblue')
    
# 3. Hydraulic Gradient Surface

HGLX=list()
HGLY=list()
HGLZ=list()

for i in range(len(Pipes)):
    NI=Pipes[i]['NI']
    NF=Pipes[i]['NF']
    for i in range(len(Reservoirs)):
        v=Reservoirs[i]['ID']
        if v==NI:
            Xo=Reservoirs[i]['X']
            Yo=Reservoirs[i]['Y']
            Zo=Reservoirs[i]['HGL']
            HGLX.append(Xo)
            HGLY.append(Yo)
            HGLZ.append(Zo)
            break
    for i in range(len(Nodes)):
        v=Nodes[i]['ID']
        if v==NI:
            Xo=Nodes[i]['X']
            Yo=Nodes[i]['Y']
            Zo=Nodes[i]['HGL']
            HGLX.append(Xo)
            HGLY.append(Yo)
            HGLZ.append(Zo)
            break
    for i in range(len(Reservoirs)):
        v=Reservoirs[i]['ID']
        if v==NF:
            Xf=Reservoirs[i]['X']
            Yf=Reservoirs[i]['Y']
            Zf=Reservoirs[i]['HGL']
            HGLX.append(Xf)
            HGLY.append(Yf)
            HGLZ.append(Zf)
            break
    for i in range(len(Nodes)):
        v=Nodes[i]['ID']
        if v==NF:
            Xf=Nodes[i]['X']
            Yf=Nodes[i]['Y']
            Zf=Nodes[i]['HGL']
            HGLX.append(Xf)
            HGLY.append(Yf)
            HGLZ.append(Zf)
            break 
    for i in range(10):
        HGLX.append(Xo+(i/10)*(Xf-Xo))
        HGLY.append(Yo+(i/10)*(Yf-Yo))
        HGLZ.append(Zo+(i/10)*(Zf-Zo))

Xmax=max(HGLX)
Ymax=max(HGLY)
Xmin=min(HGLX)
Ymin=min(HGLY)

# Please specify desired step size
# Step size must be equal in both sides

grid_x , grid_y=np.mgrid[Xmin:Xmax:50,Ymin:Ymax:50]

HGLInt1=griddata((HGLX,HGLY),HGLZ,(grid_x,grid_y),method='linear')
HGLInt2=np.nan_to_num(HGLInt1, copy=True, nan=0.0, posinf=None, neginf=None)
surf=ax.plot_surface(grid_x,grid_y,HGLInt1,cmap=cm.YlOrRd,vmin=np.nanmin(HGLInt1), vmax=np.nanmax(HGLInt1),rcount=200, ccount=200)

wb1 = xlrd.open_workbook(loc1) 
sheet1 = wb1.sheet_by_index(0)

Nodes1=list()

for i in range(NumNodes):
    Var=dict()
    Var['ID']=sheet1.cell_value(i+1,0)
    Var['X']=sheet1.cell_value(i+1,1)
    Var['Y']=sheet1.cell_value(i+1,2)
    Var['Z']=sheet1.cell_value(i+1,3)
    Var['Q']=sheet1.cell_value(i+1,4)
    Var['HGL']=sheet1.cell_value(i+1,5)
    Nodes1.append(Var)

Reservoirs1=list()

for i in range(NumReservoirs):
    Var=dict()
    Var['ID']=sheet1.cell_value(i+1,7)
    Var['X']=sheet1.cell_value(i+1,8)
    Var['Y']=sheet1.cell_value(i+1,9)
    Var['Z']=sheet1.cell_value(i+1,10)
    Var['HGL']=sheet1.cell_value(i+1,11)
    Reservoirs1.append(Var)

HGLX1=list()
HGLY1=list()
HGLZ1=list()

for i in range(len(Pipes)):
    NI=Pipes[i]['NI']
    NF=Pipes[i]['NF']
    for i in range(len(Reservoirs1)):
        v=Reservoirs1[i]['ID']
        if v==NI:
            Xo=Reservoirs1[i]['X']
            Yo=Reservoirs1[i]['Y']
            Zo=Reservoirs1[i]['HGL']
            HGLX1.append(Xo)
            HGLY1.append(Yo)
            HGLZ1.append(Zo)
            break
    for i in range(len(Nodes1)):
        v=Nodes1[i]['ID']
        if v==NI:
            Xo=Nodes1[i]['X']
            Yo=Nodes1[i]['Y']
            Zo=Nodes1[i]['HGL']
            HGLX1.append(Xo)
            HGLY1.append(Yo)
            HGLZ1.append(Zo)
            break
    for i in range(len(Reservoirs1)):
        v=Reservoirs[i]['ID']
        if v==NF:
            Xf=Reservoirs1[i]['X']
            Yf=Reservoirs1[i]['Y']
            Zf=Reservoirs1[i]['HGL']
            HGLX1.append(Xf)
            HGLY1.append(Yf)
            HGLZ1.append(Zf)
            break
    for i in range(len(Nodes1)):
        v=Nodes[i]['ID']
        if v==NF:
            Xf=Nodes1[i]['X']
            Yf=Nodes1[i]['Y']
            Zf=Nodes1[i]['HGL']
            HGLX1.append(Xf)
            HGLY1.append(Yf)
            HGLZ1.append(Zf)
            break 
    for i in range(10):
        HGLX1.append(Xo+(i/10)*(Xf-Xo))
        HGLY1.append(Yo+(i/10)*(Yf-Yo))
        HGLZ1.append(Zo+(i/10)*(Zf-Zo))

Xmax1=max(HGLX1)
Ymax1=max(HGLY1)
Xmin1=min(HGLX1)
Ymin1=min(HGLY1)

# Please specify desired step size
# Step size must be equal in both sides

grid_x1 , grid_y1=np.mgrid[Xmin1:Xmax1:50,Ymin1:Ymax1:50]

HGLInt11=griddata((HGLX1,HGLY1),HGLZ1,(grid_x1,grid_y1),method='linear')
HGLInt21=np.nan_to_num(HGLInt11, copy=True, nan=0.0, posinf=None, neginf=None)
surf1=ax1.plot_surface(grid_x1,grid_y1,HGLInt11,cmap=cm.YlOrRd,vmin=np.nanmin(HGLInt11), vmax=np.nanmax(HGLInt11),rcount=200, ccount=200)

#cbaxes = fig.add_axes([0.8, 0.1, 0.03, 0.8]) 
cbar=plt.colorbar(surf,ax=ax,shrink=0.5)
cbar.set_label('HGS [m]', labelpad=-40, y=1.05, rotation=0,fontsize=12)
cbar.ax.tick_params(labelsize=12)
cbar1=plt.colorbar(surf1,ax=ax1,shrink=0.5)
cbar1.set_label('HGS [m]', labelpad=-40, y=1.05, rotation=0,fontsize=12)
cbar1.ax.tick_params(labelsize=12)

#fig.tight_layout()


# Please specify rotation (elevation angle, azimuth angle)
# Delete # symbol before ax.view_init to allow Python to run the instruction

ax.view_init(10,130)
ax1.view_init(10,130)

ax.set_xlim(Xmin,Xmax)
ax.set_ylim(Ymin,Ymax)
ax.set_xlabel('X [m]',fontsize=12,labelpad=20)
ax.set_ylabel('Y [m]',fontsize=12,labelpad=20)
ax.set_zlabel('Z [m]',fontsize=12,labelpad=20)
ax.set_yticks([800,1200,1600,2000,2400])
ax.set_yticklabels([800,1200,1600,2000,2400],ha='center')
ax.set_xticks([1000,1500,2000,2500])
ax.set_xticklabels([1000,1500,2000,2500],ha='center')
ax.tick_params(axis='both', which='major', labelsize=12,direction='out')

ax1.set_xlim(Xmin1,Xmax1)
ax1.set_ylim(Ymin1,Ymax1)
ax1.set_xlabel('X [m]',fontsize=12,labelpad=20)
ax1.set_ylabel('Y [m]',fontsize=12,labelpad=20)
ax1.set_zlabel('Z [m]',fontsize=12,labelpad=20)
ax1.set_yticks([800,1200,1600,2000,2400])
ax1.set_yticklabels([800,1200,1600,2000,2400],ha='center')
ax1.set_xticks([1000,1500,2000,2500])
ax1.set_xticklabels([1000,1500,2000,2500],ha='center')
ax1.tick_params(axis='both', which='major', labelsize=12,direction='out')

ax.set_title('(a)')
ax1.set_title('(b)')
#fig.subplots_adjust(top=0.95)
plt.tight_layout()
plt.savefig('Fig_9.tiff', dpi=600,bbox_inches='tight')



