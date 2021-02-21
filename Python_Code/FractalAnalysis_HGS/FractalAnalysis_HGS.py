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

gs = gridspec.GridSpec(4,2)

# User Input

# Please specify the path to the Excel spreadsheet file to be opened

loc = (r'--Specify here--')

# Please specify step size according to the network

# Two Loops - 10
# Two Reservoirs - 50
# Taichung - 5
# Jilin - 5
# Hanoi - 5
# Blacksburg - 50
# New York Tunnels - 50
# BakRyan - 50
# Fossolo - 25
# R28 - 10
# Pescara - 20
# Modena - 50
# Balerma - 10
# La Uribe - 50
# El Overo - 25
# San Vicente - 0.25
# Cazucá - 25
# Elevada - 0.25
# Andalucía Alta - 30
# La Cumbre - 50
# Andalucía Baja - 50
# Toro - 50
# Candelaria - 20
# Bugalagrande - 15
# Carmen del Viboral - 50
# Morrorico Bajo - 25
# Chinú - 50
# La Enea - 25

StepSize=10


# ------------------------------------

# 1. Reading data

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
    
fig=plt.figure(dpi=600)
ax = fig.add_subplot(gs[0:2, 0:3],projection='3d')
fig.set_size_inches(15, 15)
ax.scatter(NodesX, NodesY, NodesZ, c='black', marker='o', alpha=1)

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
    plt.plot(X,Y,Z,color='darkblue')  

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

grid_x , grid_y=np.mgrid[Xmin:Xmax:StepSize,Ymin:Ymax:StepSize]

HGLInt1=griddata((HGLX,HGLY),HGLZ,(grid_x,grid_y),method='linear')
HGLInt2=np.nan_to_num(HGLInt1, copy=True, nan=0.0, posinf=None, neginf=None)
surf=ax.plot_surface(grid_x,grid_y,HGLInt1,cmap=cm.YlOrRd,vmin=np.nanmin(HGLInt1), vmax=np.nanmax(HGLInt1),rcount=200, ccount=200)

cbar=plt.colorbar(surf,ax=ax,shrink=0.7)
cbar.set_label('HGS [m]', labelpad=-40, y=1.05, rotation=0,fontsize=15)
cbar.ax.tick_params(labelsize=15)

fig.tight_layout()
fig.subplots_adjust(top=0.98)

#
#
#

# Please specify rotation (elevation angle, azimuth angle) of generated figure if desired
# Delete # symbol before ax.view_init to allow Python to run the instruction

#ax.view_init(25,100)

#
#
#

ax.set_xlim(Xmin,Xmax)
ax.set_ylim(Ymin,Ymax)
ax.set_xlabel('X [m]',fontsize=15,labelpad=20)
ax.set_ylabel('Y [m]',fontsize=15,labelpad=20)
ax.set_zlabel('Z [m]',fontsize=15,labelpad=20)
ax.tick_params(axis='both', which='major', labelsize=12)
plt.tight_layout()
plt.savefig('HGS_Surface.tiff', dpi=600,bbox_inches='tight')

# 4. Digital Elevation Model

plt.figure(2,dpi=600)
extent=[Xmin,Xmax,Ymin,Ymax]
plt.imshow(HGLInt1.T,cmap='YlOrRd',origin='lower',extent=extent)

ax = plt.gca()
ax1= plt.gca()
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05)

ax1.grid(True,color='black',linestyle='dotted')
ax1.set_xlabel('X [m]')
ax1.set_ylabel('Y [m]')
plt.colorbar(shrink=0.8,cax=cax).set_label('HGS [m]', labelpad=25,y=0.6, rotation=0,fontsize=10)
plt.savefig('DEM_Surface.tiff', dpi=600)

# 5. Fractal Dimension - Variation Estimator

numrows=len(HGLInt2)
numcols=len(HGLInt2[0])
Rmax=math.floor((min(numrows,numcols)-1)/2)

def cal_var(HGLInt2,L,X,Y):
    mtx=HGLInt2[Y:Y+L,X:X+L]
    max_val=np.max(mtx)
    if max_val==0:
        VR=math.nan
    else:
        min_val=np.min(mtx[np.nonzero(mtx)])
        VR=max_val-min_val
    return VR

Radius=list()
Variation=list()

for R in range(1,Rmax):
    L=2*R+1
    NDH=numrows-L+1
    NDV=numcols-L+1
    ad=0
    el=0
    for j in range(NDH):
        for k in range(NDV):
            var=cal_var(HGLInt2,L,k,j)
            if math.isnan(var) == False:
                ad=ad+var
                el=el+1
    Ve=float(ad/el)
    Variation.append(Ve)
    Radius.append(R)

LogVe=np.log10(Variation)
LogRad=np.log10(Radius)
mVar,bVar,rVar,pVar,stdVar=linregress(LogRad,LogVe)
CDVar=rVar**2

plt.figure(3,dpi=1200)
DVar=3-mVar
LY=mVar*LogRad+bVar
plt.plot(LogRad,LY,color='darkred',linestyle='dotted')
plt.scatter(LogRad,LogVe,s=15)
plt.xlabel('log $\epsilon$')
plt.ylabel('log V($\epsilon$)')
plt.tight_layout()

textstr = '\n'.join((
    r'$D=%.4f$' % (DVar, ),
    r'$b=%.4f$' % (bVar, ),
    r'$R$'+chr(0x00b2)+'$=%.2f$' % (CDVar, )))
props = dict(boxstyle='round', facecolor='None', alpha=0.5)
plt.text(0, 0.5, textstr, fontsize=8, bbox=props)
plt.savefig('FractalAnalysis_Surface.tiff', dpi=1200)
plt.show()

# 6. Saving results

f= open("FractalAnalysisResults_Surface.txt","w+")
f.write("Fractal Dimension Surface (D) = %s\n"%DVar)
f.write("Y-Intercept (b) = %s\n"%bVar)
f.write("R2 = %s\n"%CDVar)
f.write("log V(e)\n")
for i in LogVe:
    f.write("%s\n" % i)
f.write("log e\n")
for i in LogRad:
    f.write("%s\n" % i)    
     
f.close() 