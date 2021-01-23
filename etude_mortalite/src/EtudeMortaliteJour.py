'''
Created on 23 janv. 2021

@author: vddu
'''

if __name__ == '__main__':
    pass

#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import re
import matplotlib.pyplot as plt
import requests

# de 2000 à 2020 courbe mensuel pour véririer la saisonalité de la mortalité
# Constat 2 pic en 2020 correspondant à l'influence du covid 19 sur la mortalité.

os.chdir("/home/vddu/work-python/python-suite")

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def get_age(x):
    a = int(x[0:4])
    b = int(x[8:12])
    return b-a

def corr(v):
    for i in range(1,len(v)-1):
        if np.isnan(v[i]):
            v[i] = (v[i+1]+v[i-1])//2
        if v[i] < 500:
            v[i] = (v[i+1]+v[i-1])//2
    return v
u = pd.read_csv('covid/dc/dc_jours.csv', sep='|')

#title = 'jours|i2000|i2001|i2002|i2003|i2004|i2005|i2006|i2007|i2008|i2009|i2010|i2011|i2012|i2013|i2014|i2015|i2016|i2017|i2018|i2019|i2020'+os.linesep
#with open('covid/dc/dc_jours.csv','w') as w:
#    w.write(title)
u['jours'] = u['jours'].apply(lambda x: str(x) if x > 999 else '0'+str(x))
u['mois'] = u['jours'].apply(lambda x: x[0:2])
u['jour'] = u['jours'].apply(lambda x: x[2:4])
#print(u.head(5))
for i in range(21):
    s = str(i)
    if i < 10:
        s = '0'+s
    u['i20'+s] = corr(u['i20'+s])

v = u[['jours','i2000','i2001','i2002','i2003','i2004','i2005',
        'i2006','i2007','i2008','i2009','i2010','i2011','i2012',
        'i2013','i2014','i2015','i2016','i2017','i2018','i2019']]
#v = u.copy()
print(v.head())
print(v.iloc[120:171][:])
w = v.std(axis=1)
print(w)
m2019 = v['i2019'].mean()
v = v.mean(axis=1)
v = corr(v)
mm = v.mean()
ecart = w.mean()
print("ecart ",ecart)
print(v)
#v.columns = ['mean']
v.rename_axis("mean")
v = v+(m2019-mm)
z = v+ecart
di = u['i2020']-z
di = di.iloc[0:334]
di = di.apply(lambda x: x if x >= 0 else 0)
diff = di.sum()
print('diff :',diff)
d1 = di.iloc[0:180]
d2 = di.iloc[180:]
d1ff = d1.sum()
d2ff = d2.sum()
print('d1 :',d1ff)
print('d2 :',d2ff)
print('diff :',diff)


#print(type(v))
#print(v.head())
#u.plot(x='jours')

#plt.plot(u['jours'], u['i2000'], 'b',
#         u['jours'], u['i2001'], 'b')
figure = plt.figure(figsize = (10, 5))
axes = figure.add_subplot(111)
#axes.scatter(range(5), [x ** 2 for x in range(5)], s = 50)

axes.set_frame_on(False)
axes.yaxis.tick_left()
axes.xaxis.set_visible(True)
#(xmin, xmax) = axes.xaxis.get_view_interval()
#(ymin, ymax) = axes.yaxis.get_view_interval()
(xmin, xmax, ymin, ymax) = plt.axis()

#axes.add_artist(plt.Line2D((0, 0), (0, ymax), color = 'magenta', linewidth = 1))
#axes.add_artist(plt.Line2D((0, 0), (ymax, 0), color = 'cyan', linewidth = 1))
"""
axes.xaxis.set_ticklabels(['                                Janvier',
'                               Février',
'                               Mars',
'                               Avril',
'                               Mai',
'                               Juin',
'                               Juillet',
'                               Aout',
'                               Sepembre',
'                               Octobre',
'                               Novembre',
'                               Décembre'])
"""
axes.xaxis.set_ticklabels(['',
'Janvier',
'Février',
'Mars',
'Avril',
'Mai',
'Juin',
'Juillet',
'Aout',
'Sepembre',
'Octobre',
'Novembre',
'Décembre'])
#axes.xaxis.set_ticklabels(np.arange(0,13))

axes.xaxis.grid(True, color = 'orange', linewidth = 1, linestyle = 'dashed')
axes.yaxis.grid(True, color = 'orange', linewidth = 1, linestyle = 'dashed')
#axes.yaxis.grid(True, which = 'minor', color = 'orange', linewidth = 1, linestyle = 'dotted')

pl = axes.plot(
         u['jours'], u['i2019'], 'silver',
         u['jours'], u['i2020'], 'r',
         u['jours'], v, 'g',
         u['jours'], z, '#88FF88')

start, end = axes.get_xlim()
axes.set_xlabel("jours de l'année")
axes.set_ylabel('nombre de décès')

axes.set_frame_on(True)
#axes.set_xlim(0, 11)
axes.xaxis.set_ticks_position('bottom')
axes.xaxis.set_label_position('bottom')

locs, labels = plt.xticks()
print(len(locs))
print(len(labels))
axes.xaxis.set_ticks(np.arange(start, end, (end-start)/13))

#plt.legend([pl], ['2019','2020'])
#plt.legend([pl], ['2019','2020'], loc = 'lower left',
#    ncol = 2, scatterpoints = 1,
#    frameon = True, markerscale = 2,
#    title = 'légende',
#    borderpad = 0.5,
#    labelspacing = 0.5)
#axes.legend(bbox_to_anchor = (1, 20), loc = 'upper right', prop = {'size': 50})

leg = [str(x) for x in range(2019,2021)]
leg = ['2019','2020','Moyenne de 2000 à 2020 corrigée','Moyenne + écart type']
axes.legend(pl, leg, title = 'légende', prop = {'size': 20},ncol =2)
plt.title("mortalité de 2019 comparée à 2020")

plt.show()
