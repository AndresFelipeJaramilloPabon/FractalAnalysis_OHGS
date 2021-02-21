# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:54:27 2021

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

Costs=[815700571,
830890363,
835184638,
1173393576,
1360870614,
1639003136,
1678996204,
1827025598,
2584058160,
3796220689,
5651909421,
]

labels=['LC',
'NO1',
'NO2',
'NO3',
'NO4',
'NO5',
'NO6',
'NO7',
'NO8',
'NO9',
'NO10',
]


fig,ax=plt.subplots(dpi=300)
fig.set_size_inches(8.5,3)
x = np.arange(len(labels))
bars = ax.bar(x, Costs,width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(labels,{'size':11})
ax.set_ylabel('Cost (COP)',{'size':11})
ax.set_ylim(0,6500000000)
ax.set_yticks(np.arange(0, 7000000000, 2000000000))
ax.set_yticklabels(['${:,.0f}'.format(int(x)/1000000)+'M' for x in ax.get_yticks().tolist()],{'size':11})

def label_bars(bars):
    for i in bars:
        height = i.get_height()
        ax.annotate('${:,.0f}'.format(height/1000000),
                    xy=(i.get_x() + i.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')

label_bars(bars)

textstr = '\n'.join((
    r'LC = Least Cost',
    r'NO = Non-Optimal'))
props = dict(boxstyle='round', facecolor='None', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
plt.tight_layout()
plt.savefig('Fig_6.tiff', dpi=600,bbox_inches = 'tight')
