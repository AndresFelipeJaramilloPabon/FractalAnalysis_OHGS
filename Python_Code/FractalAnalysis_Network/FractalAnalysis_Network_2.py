# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 13:54:37 2020

@author: Andrés Jaramillo
"""
import xlrd
from scipy.stats import linregress
import numpy as np
from scipy.sparse.csgraph import shortest_path
import matplotlib.pyplot as plt 
from matplotlib import cm
from PIL import Image
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from operator import itemgetter

# User input 

# Please specify the path to the Excel spreadsheet file to be opened
# Note that the following algorithm was used for Water Distribution Networks with more than 250 nodes

loc = (r'--Specify here--')

# Please specify calculation criterion

# Topology - 1
# Flow - 2
# Energetical - 3
# Infrastructural - 4

w=1

# --------------------------------------

# 1. Reading data

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

# 2. Data Storage
NumNodos=int(sheet.cell_value(0,22))
NumEmbalses=int(sheet.cell_value(1,22))
NumTuberias=int(sheet.cell_value(2,22))

NyE=list() # Nodes (including reservoirs)

for i in range(NumNodos):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,0)
    Var['X']=sheet.cell_value(i+1,1)
    Var['Y']=sheet.cell_value(i+1,2)
    Var['Z']=sheet.cell_value(i+1,3)
    Var['LGH']=sheet.cell_value(i+1,5)
    Var['W']=0
    Var['Free']=0
    NyE.append(Var)

for i in range(NumEmbalses):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,7)
    Var['X']=sheet.cell_value(i+1,8)
    Var['Y']=sheet.cell_value(i+1,9)
    Var['Z']=sheet.cell_value(i+1,10)
    Var['LGH']=sheet.cell_value(i+1,11)
    Var['W']=0
    Var['Free']=0
    NyE.append(Var)

Tuberias=list() # Pipes

for i in range(NumTuberias):
    Var=dict()
    Var['ID']=sheet.cell_value(i+1,13)
    Var['NIyNF']=[sheet.cell_value(i+1,14),sheet.cell_value(i+1,15)]
    Var['D']=sheet.cell_value(i+1,16)
    Var['Q']=sheet.cell_value(i+1,19)
    Tuberias.append(Var)
    
# 3. Renaming elements

aR=0
for i in NyE:
    aR=aR+1
    i['ID']=aR
    for j in Tuberias:
        if j['NIyNF'][0]==i['ID']:
            j['NIyNF'][0]=aR
        elif j['NIyNF'][1]==i['ID']:
            j['NIyNF'][1]=aR

# 3. Initialization
    
NE=NumNodos+NumEmbalses
logNB=list()
logLB=list()

# 4. Graph Builder
    
graph=dict()
for i in NyE:
    Var=list()
    for j in Tuberias:
        try:
            v=j['NIyNF'].index(i['ID'])
        except ValueError:
            v=-1
        if v==0:
            Var.append(j['NIyNF'][1])
        elif v==1:
            Var.append(j['NIyNF'][0])  
    graph[i['ID']]=Var
    
A=np.zeros((NE,NE))

for i in range(NE):
    for j in range(NE):
        a=0
        for t in Tuberias:
            if (i+1) in t['NIyNF'] and (j+1) in t['NIyNF']:
                a=1
        if i==j:
            a=0
        A[i][j]=a


SD=shortest_path(A,method='D',directed=False)

# 5. Weight - Individual Nodes

def indweight_calculator(i,w):
    W=0
    if w==1:
        W=1
    elif w==2:
        pipes=[k for k in Tuberias if i in k['NIyNF']]
        for k in pipes:
            if k['Q']>0 and i==k['NIyNF'][1]:
                W=W+k['Q']
            elif k['Q']<0 and i==k['NIyNF'][0]:
                W=W-k['Q']
    elif w==3:
        for k in NyE:
            if i==k['ID']:
                W=k['LGH']
    elif w==4:
        for k in graph[i]:
            for m in Tuberias:
                if i in m['NIyNF'] and k in m['NIyNF']:
                    W=W+m['D']
    return W

for i in NyE:
    i['W']=indweight_calculator(i['ID'],w)
    
# 6. Box-Covering Algorithm

def box_builder(node,step):
    box=list()
    nd=np.where(SD[int(node)-1]<=step)[0]+1
    w=[i for i in NyE if i['ID']==node][0]['W']
    for i in nd:
        f=[item for item in NyE if item['ID']==i]
        if f[0]['Free'] == 0:
            box.append(i)
            w=w+f[0]['W']
    return box,w

Step=list()
NBVect=list()
LBVect=list()

LBVect.append(1)
if np.ceil(np.sqrt(NE))%2==0:
    LBmax=np.ceil(np.sqrt(NE)-1)
else:
    LBmax=np.ceil(np.sqrt(NE))
LBVect.append(LBmax)
LBVect.insert(1,LBmax-2)
LBVect.insert(1,LBmax-4)
LBVect.insert(1,LBmax-6)
LBVect.insert(1,LBmax-8)
LBVect.insert(1,LBmax-10)

for s in LBVect:
    NB=0
    FU=NE
    for i in NyE:
        i['Free']=0
    step=(s-1)/2
    Step.append(step)
    W=0
    Box=list()
    if step==0:
        NB=NE
        logNB.append(np.log10(NB))
        logLB.append(np.log10(s))
        NBVect.append(NB)
    else:
        while FU>0:
            for j in NyE:
                if j['Free']==0:
                    box,w=box_builder(j['ID'],step)     
                if w>W:
                    W=w
                    Box=box
            if Box:
                NB=NB+1
                FU=FU-len(Box)
                for i in NyE:
                    if i['ID'] in Box:
                        i['Free']=1;
            W=0
        NBVect.append(NB)
        logNB.append(np.log10(NB))
        logLB.append(np.log10(s))

# 7. Linear Regression
        
mBC,bBC,rBC,pBC,sBC=linregress(logLB,logNB)
FractalDimension=-mBC

CD=rBC**2

# 8. Graph and results

plt.figure(1,figsize=[3.5,3.5],dpi=1200)
LY=mBC*np.array(logLB)+bBC
plt.plot(logLB,LY,color='darkred',linestyle='dotted')
plt.scatter(logLB,logNB,s=15)
plt.xlabel('log $l_B$')
plt.ylabel('log $N_B$')
plt.tight_layout()

textstr = '\n'.join((
    r'$D=%.4f$' % (FractalDimension, ),
    r'$R$'+chr(0x00b2)+'$=%.2f$' % (CD, )))
props = dict(boxstyle='round', facecolor='None', alpha=0.5)
plt.text(0, 0.5, textstr, fontsize=8, bbox=props)
plt.savefig('FractalAnalysis_Network.tiff', dpi=1200)
plt.show()

f= open("FractalAnalysisResults_Network.txt","w+")
f.write("Fractal Dimension Network (D) = %s\n"%FractalDimension)
f.write("R2 = %s\n"%CD)
f.write("log NB\n")
for i in logNB:
    f.write("%s\n" % i)
f.write("log LB\n")
for i in logLB:
    f.write("%s\n" % i)    
     
f.close()

print(FractalDimension)
print(CD)
