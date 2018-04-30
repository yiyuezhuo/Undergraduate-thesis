# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 09:59:03 2018

@author: yiyuezhuo
"""

with open('!HISTORICAL 1.2 Gettysburg - July 2, 1863.scn') as f:
    code = f.read()
    
code_line = code.split('\n')

units = []

for line in code_line[13:]:
    symbols = line.split(' ')
    if symbols[0] != '1':
        break
    symbols = symbols[1:]
    unit = dict(symbol = symbols)
    unit['id'] = [int(n) for n in symbols[0].split('.')]
    unit['number'] = int(symbols[3])
    unit['i'] = int(symbols[-2])
    unit['j'] = int(symbols[-1]) 
    #他这个坐标系既不是直角坐标系也不是矩阵坐标系，应该算屏幕坐标系，即xy中y倒过来
    units.append(unit)
    

    
class OOBNode:
    def __init__(self, master):
        self.value = None
        self.type = None
        self.children = []
        self.master =  master
    def __repr__(self, pad=0):
        if self.value == None:
            name = 'root'
        elif 'name' not in self.value:
            name = '~'
        else:
            name = ' '*pad + self.value['name']
        lines = [name]
        for child in self.children:
            lines.append(child.__repr__(pad=pad+1))
        return '\n'.join(lines)
    def __getitem__(self, key):
        return self.children[key]
            
'''
def parseOOB(state):
    lines = state['lines']
    i = state['i']
    
    if i>=len(lines):
        return
    
    node = OOBNode()
    
    code = lines[i].strip().split(' ')
    if code[0] in ['U','L','S']:
        node.type = code[0]
        if code[0] == 'U':
            value = {}
            value['number'] = int(code[1])
            value['type'] = code[3]
            value['name'] = ' '.join(code[7:])
            node.value = value
        elif code[0] == 'L':
            value = {}
            value['command'] = int(code[1])
            value['leadership'] = int(code[2])
            value['name'] = ' '.join(code[4:])
        elif code[0] == 'S'
    
    while True:
        line = lines[i].strip()
        i +=1
        if line == 'End':
            state['i'] = i
            return node
        symbols = line.split(' ')
        p
        if symbols[0] == ''
'''
def parseOOB(lines):
    root = OOBNode(None)
    stack = [root]
    current_side = None
    for line in lines:
        
        line = line.strip()
        
        if line == 'Begin':
            stack.append(stack[-1].children[-1])
            continue
        elif line == 'End':
            stack.pop()
            continue
        
        node = OOBNode(stack[-1])
        
        if line.startswith('Union'):
            current_side = 'Union'
            line = ' '.join(line.split(' ')[1:])
        elif line.startswith('Confederate'):
            current_side = 'Confederate'
            line = ' '.join(line.split(' ')[1:])
        
        code = line.split(' ')
        node.type = code[0]
        
        value = {'side':current_side }
        if code[0] == 'U':
            value['number'] = int(code[1])
            value['type'] = code[3]
            value['name'] = ' '.join(code[7:])
        elif code[0] == 'L':
            value['command'] = int(code[1])
            value['leadership'] = int(code[2])
            value['name'] = ' '.join(code[4:])
        elif code[0] == 'S':
            value['name'] = ' '.join(code[3:])
        elif code[0] in ['A','C','D','B']:
            value['name'] = ' '.join(code[1:])
        elif code[0] == '': ## null line
            continue
        else:
            raise NotImplementedError
        node.value = value
        
        stack[-1].children.append(node)
    
    return root
        
with open('Gettysburg4.oob') as f:
    lines = f.read().split('\n')
    
oob = parseOOB(lines[1:]) # remove unknown tag 3

def select(oob,id):
    item = oob
    for i in id:
        item = item[i-1]
    return item
    
def link(units,oob):
    for unit in units:
        unit['unit'] = select(oob, unit['id'])
        unit['name'] = unit['unit'].value['name']
        unit['side'] = unit['unit'].value['side']
        unit['unit'].value['scr_unit'] = unit
        
link(units,oob)