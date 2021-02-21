# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 20:29:22 2021

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

Surface=[2.0333,
2.1029,
2.0723,
2.1343,
2.0214,
2.3388,
2.0381,
2.0894,
2.2121,
2.0647,
2.3125,
2.3204,
2.2982,
2.0064,
2.2110,
1.9386,
2.1754,
2.0338,
2.0703,
2.1971,
2.0617,
2.1202,
1.9283,
2.1394,
2.0764,
2.0583,
1.8622,
2.0834,
]
Surface=np.asarray(Surface)

Topology=[1.1981,
1.2319,
1.3134,
1.3944,
1.2108,
1.4158,
1.0537,
1.3018,
1.4396,
1.3464,
0.5923,
1.2362,
0.5862,
1.0720,
1.2256,
0.1141,
1.1759,
1.0384,
1.2735,
1.1665,
1.1868,
1.2386,
1.2369,
1.3410,
0.3293,
0.2041,
1.4631,
1.1312,
]
Topology=np.asarray(Topology)

Flow=[0.9428,
1.0517,
1.0908,
1.1686,
1.0698,
1.4307,
1.0524,
1.0899,
1.2940,
1.2738,
0.9252,
1.2085,
0.5712,
1.1575,
1.2443,
0.6192,
1.2397,
0.9816,
1.3054,
1.1153,
1.1863,
1.0582,
1.2084,
1.2806,
0.3243,
0.4030,
1.4533,
1.0871,
]
Flow=np.asarray(Flow)

HGL=[1.1394,
1.2319,
1.2768,
1.3755,
1.2107,
1.4158,
1.0617,
1.3018,
1.4495,
1.3220,
0.6105,
1.2489,
0.5877,
1.1274,
1.2163,
0.1120,
1.1652,
1.0108,
1.2747,
1.1541,
1.1830,
1.2351,
1.2441,
1.3435,
0.3266,
0.2041,
1.4533,
1.1321,
]
HGL=np.asarray(HGL)

Diameters=[1.0977,
1.0317,
1.2996,
1.2517,
1.2208,
1.4059,
1.0296,
1.3073,
1.4495,
1.2980,
0.8867,
1.2676,
0.5787,
1.1191,
1.1902,
0.6558,
1.1392,
1.0016,
1.2347,
1.1456,
1.1235,
1.1736,
1.2167,
1.3184,
0.3277,
0.2042,
1.4533,
1.1159,
]
Diameters=np.asarray(Diameters)

s1,i1,r1,p1,st1=linregress(Topology,Surface)
L1=s1*Topology+i1
s2,i2,r2,p2,st2=linregress(Flow,Surface)
L2=s2*Flow+i2
s3,i3,r3,p3,st3=linregress(HGL,Surface)
L3=s3*HGL+i3
s4,i4,r4,p4,st4=linregress(Diameters,Surface)
L4=s4*Diameters+i4

SurfaceEuc=np.zeros((28,28))
TopologyEuc=np.zeros((28,28))
FlowEuc=np.zeros((28,28))
EnergyEuc=np.zeros((28,28))
DiametersEuc=np.zeros((28,28))

for i in range(28):
    for j in range(28):
        SurfaceEuc[i][j]=abs(Surface[i]-Surface[j])
        TopologyEuc[i][j]=abs(Topology[i]-Topology[j])
        FlowEuc[i][j]=abs(Flow[i]-Flow[j])
        EnergyEuc[i][j]=abs(HGL[i]-HGL[j])
        DiametersEuc[i][j]=abs(Diameters[i]-Diameters[j])

SurfaceCen=np.zeros((28,28))
TopologyCen=np.zeros((28,28))
FlowCen=np.zeros((28,28))
EnergyCen=np.zeros((28,28))
DiametersCen=np.zeros((28,28))

MeanSurface=np.mean(SurfaceEuc)
MeanTopology=np.mean(TopologyEuc)
MeanFlow=np.mean(FlowEuc)
MeanEnergy=np.mean(EnergyEuc)
MeanDiameters=np.mean(DiametersEuc)

MeanRowSurface=SurfaceEuc.mean(axis=1)
MeanRowTopology=TopologyEuc.mean(axis=1)
MeanRowFlow=FlowEuc.mean(axis=1)
MeanRowEnergy=EnergyEuc.mean(axis=1)
MeanRowDiameters=DiametersEuc.mean(axis=1)

MeanColSurface=SurfaceEuc.mean(axis=0)
MeanColTopology=TopologyEuc.mean(axis=0)
MeanColFlow=FlowEuc.mean(axis=0)
MeanColEnergy=EnergyEuc.mean(axis=0)
MeanColDiameters=DiametersEuc.mean(axis=0)

for i in range(28):
    for j in range(28):
        SurfaceCen[i][j]=SurfaceEuc[i][j]-MeanColSurface[j]-MeanRowSurface[i]+MeanSurface
        TopologyCen[i][j]=TopologyEuc[i][j]-MeanColTopology[j]-MeanRowTopology[i]+MeanTopology
        FlowCen[i][j]=FlowEuc[i][j]-MeanColFlow[j]-MeanRowFlow[i]+MeanFlow
        EnergyCen[i][j]=EnergyEuc[i][j]-MeanColEnergy[j]-MeanRowEnergy[i]+MeanEnergy
        DiametersCen[i][j]=DiametersEuc[i][j]-MeanColDiameters[j]-MeanRowDiameters[i]+MeanDiameters
    
CovST=np.sqrt(sum(sum(np.multiply(SurfaceCen,TopologyCen)))/(28**2))
CovSF=np.sqrt(sum(sum(np.multiply(SurfaceCen,FlowCen)))/(28**2))
CovSE=np.sqrt(sum(sum(np.multiply(SurfaceCen,EnergyCen)))/(28**2))
CovSD=np.sqrt(sum(sum(np.multiply(SurfaceCen,DiametersCen)))/(28**2))

VarS=np.sqrt(sum(sum(np.multiply(SurfaceCen,SurfaceCen)))/(28**2))
VarF=np.sqrt(sum(sum(np.multiply(FlowCen,FlowCen)))/(28**2))
VarT=np.sqrt(sum(sum(np.multiply(TopologyCen,TopologyCen)))/(28**2))
VarE=np.sqrt(sum(sum(np.multiply(EnergyCen,EnergyCen)))/(28**2))
VarD=np.sqrt(sum(sum(np.multiply(DiametersCen,DiametersCen)))/(28**2))

DisCovST=CovST/np.sqrt(VarS*VarT)
DisCovSF=CovSF/np.sqrt(VarS*VarF)
DisCovSE=CovSE/np.sqrt(VarS*VarE)
DisCovSD=CovSD/np.sqrt(VarS*VarD)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,dpi=600)
fig.set_size_inches(8,4.5)
ax1.scatter(Topology,Surface,s=20)
ax1.plot(Topology,L1,c='maroon',linestyle='solid',alpha=0.7)
ax1.set(title='Topological criterion')
ax1.set_xlabel('D - Optimized Network')
ax1.set_ylabel('D - OHGS')
ax1.set_ylim(1.5,3)
ax1.grid()

textstr = '\n'.join((
    r'$\rho=%.4f$' % (pearsonr(Topology,Surface)[0], ),
    r'$dCor=%.4f$' % (DisCovST, )))
props = dict(boxstyle='round', facecolor='white')
ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

ax2.scatter(Flow,Surface,s=20)
ax2.plot(Flow,L2,c='maroon',linestyle='solid',alpha=0.7)
ax2.set(title='Flow criterion')
ax2.set_xlabel('D - Optimized Network')
ax2.set_ylabel('D - OHGS')
ax2.set_ylim(1.5,3)
ax2.grid()

textstr = '\n'.join((
    r'$\rho=%.4f$' % (pearsonr(Flow,Surface)[0], ),
    r'$dCor=%.4f$' % (DisCovSF, )))
props = dict(boxstyle='round', facecolor='white')
ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

ax3.scatter(HGL,Surface,s=20)
ax3.plot(HGL,L3,c='maroon',linestyle='solid',alpha=0.7)
ax3.set(title='Energetical criterion')
ax3.set_xlabel('D - Optimized Network')
ax3.set_ylabel('D - OHGS')
ax3.set_ylim(1.5,3)
ax3.grid()

textstr = '\n'.join((
    r'$\rho=%.4f$' % (pearsonr(HGL,Surface)[0], ),
    r'$dCor=%.4f$' % (DisCovSE, )))
props = dict(boxstyle='round', facecolor='white')
ax3.text(0.05, 0.95, textstr, transform=ax3.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

ax4.scatter(Diameters,Surface,s=20)
ax4.plot(Diameters,L4,c='maroon',linestyle='solid',alpha=0.7)
ax4.set(title='Infrastructural criterion')
ax4.set_xlabel('D - Optimized Network')
ax4.set_ylabel('D - OHGS')
ax4.set_ylim(1.5,3)
ax4.grid()

textstr = '\n'.join((
    r'$\rho=%.4f$' % (pearsonr(Diameters,Surface)[0], ),
    r'$dCor=%.4f$' % (DisCovSD, )))
props = dict(boxstyle='round', facecolor='white')
ax4.text(0.05, 0.95, textstr, transform=ax4.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('Fig_12.tiff', dpi=800,bbox_inches = 'tight')
