# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 12:11:02 2018

@author: yiyuezhuo
"""

from test import units,oob

import matplotlib.pyplot as plt
import numpy as np

divs =[unit for unit in units if unit['id'][-1] == 1 and unit['unit'].master.type == 'D']

Confederate = [[div['i'],div['j']] for div in divs if div['side'] == 'Confederate']
Confederate_name = [div['unit'].master.value['name'] for div in divs if div['side'] == 'Confederate']
Union = [[div['i'],div['j']] for div in divs if div['side'] == 'Union']
Union_name = [div['unit'].master.value['name'] for div in divs if div['side'] == 'Union']

Confederate,Union = np.array(Confederate),np.array(Union)
maxy = max(np.max(Confederate[:,1]),np.max(Union[:,1]))
Confederate[:,1] = maxy - Confederate[:,1]
Union[:,1] = maxy - Union[:,1]


plt.scatter(Confederate[:,0],Confederate[:,1],color='grey',label='Confederate')
plt.scatter(Union[:,0],Union[:,1],color='blue',label='Union')
plt.legend()
plt.show()

def show_two_side(Confederate, Union, alpha=1.0, maxy=None,
                  Confederate_label='Confederate',Union_label='Union'):
    if maxy is None:
        maxy = max(np.max(Confederate[:,1]),np.max(Union[:,1]))
    Confederate[:,1] = maxy - Confederate[:,1]
    Union[:,1] = maxy - Union[:,1]
    
    
    plt.scatter(Confederate[:,0],Confederate[:,1],color='grey',label=Confederate_label,alpha=alpha)
    plt.scatter(Union[:,0],Union[:,1],color='blue',label=Union_label,alpha=alpha)
    #plt.legend()
    
def show_level(level='D', **kwargs):
    '''D in {'A','C','D','B'}'''
    divs =[unit for unit in units if unit['id'][-1] == 1 and unit['unit'].master.type == level]
    Confederate = [[div['i'],div['j']] for div in divs if div['side'] == 'Confederate']
    Union = [[div['i'],div['j']] for div in divs if div['side'] == 'Union']
    show_two_side(np.array(Confederate), np.array(Union), **kwargs)
    
def show_name(level='D',maxy=None,show_Confederate=True,show_Union=True):
    divs =[unit for unit in units if unit['id'][-1] == 1 and unit['unit'].master.type == 'D']

    Confederate = [[div['i'],div['j'],div['unit'].master.value['name']] for div in divs if div['side'] == 'Confederate']
    Union = [[div['i'],div['j'],div['unit'].master.value['name']] for div in divs if div['side'] == 'Union']
    if maxy is None:
        maxy = np.max([div['j'] for div in divs])
    if show_Confederate:
        for i,j,name in Confederate:
            plt.text(i,maxy-j,name)
    if show_Union:
        for i,j,name in Union:
            plt.text(i,maxy-j,name)
            
def count(unit):
    if unit.type == 'U':
        if 'scr_unit' in unit.value:
            return unit.value['scr_unit']['number']
        return 0 # 未出现在scr中
    elif unit.type in ['A','C','D','B']: #不区分步兵骑兵炮兵
        _sum = 0
        for child in unit.children:
            _sum += count(child)
        return _sum
    else:
        return 0


show_level('C')
plt.title('corp distribution')
plt.legend()
plt.show()

show_level('D')
plt.title('div distribution')
show_name(show_Union=False) #Union全黏在一起看不清楚
plt.legend()
plt.show()

show_level('B')
plt.title('bde distribution')
plt.legend()
plt.show()

#show_level('C')
show_level('D', alpha=1.0,Confederate_label='CSA Div',Union_label='USA Div')
show_level('B',alpha=0.3,Confederate_label='CSA Bde',Union_label='USA Bde')
show_name(show_Union=False)
plt.legend()
plt.show()

plt.figure(figsize=(5,10))

plt.subplot(2,1,1)
show_level('B')
#plt.title('bde distribution')
#plt.legend()
plt.gca().set_title('bde distribution')

plt.subplot(2,1,2)
show_level('D')
show_name(show_Union=False) #Union全黏在一起看不清楚
#plt.title('div distribution')
#plt.legend()
plt.gca().set_title('div distribution')

plt.legend()
plt.show()

Confederate_number  = [count(div['unit'].master) for div in divs if div['side'] == 'Confederate']
Union_number = [count(div['unit'].master) for div in divs if div['side'] == 'Union']
