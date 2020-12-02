# @Date:   2020-11-29T20:15:25+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: rotate3d.py
# @Last modified time: 2020-12-02T01:08:16+01:00



import os
import sys
import time
import math
import numpy as np
import random
import datetime as dt
from colors import color,blue, green, white, yellow,red
''' this is the ansicolors module ^^^ '''

import ctypes
from ctypes import c_long, c_ulong
gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))


def moveCursor (y, x):
   """move cursor to position indicated by x and y."""
   value = x + (y << 16)
   ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong(value))


class cell:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tile=bkg
        self.hasChanged=True
        self.type='background'
        self.frozen = False
        self.color=bkg_color
bkg=" "
bkg_color="#333333"
dot='O'
size_x,size_y = 80,50
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = 0
# origin=[center_x,center_y,center_z]
origin=[center_x,center_y,center_z,1]
#create the grid
grid = []
for y in range(size_y):
    row=[]
    for x in range(size_x):
        row.append(cell(x,y))
    grid.append(row)

'''
rotX_90 =  [x',      [cos90  -sin90  0       [x,
            y',  =    sin90  cos90   0   *    y,
            z']       0      0       1]       z]
'''

def update_screen():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            if cell.hasChanged:
                cell.hasChanged=False
                if cell.color is not None:
                    moveCursor(row,col)
                    print(color(f"{cell.tile}",cell.color))

def delete_line(p1,p2):
    draw_line(p1,p2,delete=True)

def draw_line(p1,p2,color=(255,255,255),delete=False):
    x1 = int(p1[0][0]+0.5)
    y1 = int(p1[1][0]+0.5)
    x2 = int(p2[0][0]+0.5)
    y2 = int(p2[1][0]+0.5)
    # x1,y1,x2,y2 = p1[0],p1[1],p2[0],p2[1]
    dx = x2-x1
    dy = y2-y1
    dx1=abs(dx)
    dy1=abs(dy)
    px=2*dy1-dx1
    py=2*dx1-dy1
    try:
        if dy1 <= dx1:
            if dx >= 0:
                x,y,xe=x1,y1,x2
            else:
                x,y,xe=x2,y2,x1
            cell = grid[y][x]
            cell.tile = dot if delete==False else bkg
            cell.color = color  if delete==False else bkg_color
            cell.hasChanged=True
            while x < xe:
                x+=1
                if px < 0:
                    px+=2*dy1
                else:
                    if(dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        y+=1
                    else:
                        y-=1
                    px+=2*(dy1-dx1)
                cell = grid[y][x]
                cell.tile = dot if delete==False else bkg
                cell.color = color if delete==False else bkg_color
                cell.hasChanged=True
        else:
            if dy >= 0:
                x,y,ye = x1,y1,y2
            else:
                x,y,ye = x2,y2,y1
            cell = grid[y][x]
            cell.tile = dot if delete==False else bkg
            cell.color = color if delete==False else bkg_color
            cell.hasChanged=True
            while y < ye:
                y+=1
                if py <= 0:
                    py+=2*dx1
                else:
                    if(dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        x+=1
                    else:
                        x-=1
                    py+=2*(dx1-dy1)
                cell = grid[y][x]
                cell.tile = dot if delete==False else bkg
                cell.color = color if delete==False else bkg_color
                cell.hasChanged=True
    except IndexError:
        print(f"X:{x} Y:{y}")

def drawVectorPoint(point,color,delete=False):
    x,y=int(point[0][0]+0.5),int(point[1][0]+0.5)
    cell = grid[y][x]
    cell.tile = dot if delete==False else bkg
    cell.color = color  if delete==False else bkg_color
    cell.hasChanged=True

def vectorToMatrix(vector):
    return [[p] for p in vector]

def translate_point(pivot,point):
    tx,ty,tz = pivot[0],pivot[1],pivot[2]
    translation_matrix = [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]
    return matrix_multiply(translation_matrix,point)

def matrix_multiply(a, b):
    colsA=len(a[0])
    rowsA=len(a)
    colsB=len(b[0])
    rowsB=len(b)
    # print(a)
    # print(b)
    # exit()
    if colsA != rowsB:
        print(f"matrix mismatch a:{a}\n b:{b}")
        print(len(a[0]))
        print(len(b))
        return None
    result = [[sum(x*y for x,y in zip(a_row,b_col)) for b_col in zip(*b)] for a_row in a]

    return result

def rotate_x(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    #translate
    point = translate_point(inverted_pivot,point)
    xrot=[
        [1,   0,    0  , 0],
        [0,   cos, -sin, 0],
        [0,   sin, cos , 0],
        [0,   0,    0,   1]
        ]
    #rotate
    point = matrix_multiply(xrot,point)
    #translate back
    point = translate_point(pivot,point)

    return point

def rotate_y(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    #translate
    point = translate_point(inverted_pivot,point)
    yrot=[
        [cos, 0, sin,   0],
        [0,   1, 0  ,   0],
        [-sin,0, cos,   0],
        [0,   0,    0,  1]
        ]
    #rotate
    point = matrix_multiply(yrot,point)
    #translate back
    point = translate_point(pivot,point)
    return point

def rotate_z(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    old_point = list(point)
    #translate
    point = translate_point(inverted_pivot,point)
    zrot=[
        [cos, -sin, 0,  0],
        [sin, cos,  0,  0],
        [0,   0,    1,  0],
        [0,   0,    0,  1]
        ]

    #rotate
    point = matrix_multiply(zrot,point)
    #translate back
    point = translate_point(pivot,point)

    return point

def rotate_model(model,pivot,axis,angle):
    if axis=='x':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_x(pivot,p,angle)
    if axis=='y':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_y(pivot,p,angle)
    if axis=='z':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_z(pivot,p,angle)

def undraw_model(model):
    for line in model['lines']:
        draw_line(
            model['points'][line[0]],
            model['points'][line[1]],
            color=None,
            delete=True
            )
def draw_model(model):
    for line in model['lines']:
        draw_line(
            model['points'][line[0]],
            model['points'][line[1]],
            color=line[2],
            )

my_3dmodel={
    'name':'cube',
    'x':None,
    'y':None,
    'points':[
        [[center_x-10],[center_y-10],[center_z],[1]],
        [[center_x+10],[center_y-10],[center_z],[1]],
        [[center_x+10],[center_y+10],[center_z],[1]],
        [[center_x-10],[center_y+10],[center_z],[1]],
        [[center_x-10],[center_y-10],[center_z+20],[1]],
        [[center_x+10],[center_y-10],[center_z+20],[1]],
        [[center_x+10],[center_y+10],[center_z+20],[1]],
        [[center_x-10],[center_y+10],[center_z+20],[1]]
    ],
    'lines':[
        [0,1,(0,255,0)],[1,2,(0,255,0)],[2,3,(0,255,0)],[3,0,(0,255,0)],
        [4,5,(0,0,255)],[5,6,(0,0,255)],[6,7,(0,0,255)],[7,4,(0,0,255)],
        [0,4,(0,255,255)],[1,5,(0,255,255)],[2,6,(0,255,255)],[3,7,(0,255,255)]
    ]
}

update_screen()
time.sleep(0.5)
for angle in range(360):
    time.sleep(0.05)
    undraw_model(my_3dmodel)
    update_screen()
    rotate_model(my_3dmodel,origin,'x',0.1)
    rotate_model(my_3dmodel,origin,'y',0.1)
    rotate_model(my_3dmodel,origin,'z',0.1)
    draw_model(my_3dmodel)
    update_screen()
exit()
