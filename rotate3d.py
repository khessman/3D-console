# @Date:   2020-11-29T20:15:25+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: rotate3d.py
# @Last modified time: 2020-12-02T00:01:40+01:00



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
    p_old=list(point)
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


p1 = vectorToMatrix([center_x-10,center_y-10,center_z,1])
p2 = vectorToMatrix([center_x+10,center_y-10,center_z,1])
p3 = vectorToMatrix([center_x+10,center_y+10,center_z,1])
p4 = vectorToMatrix([center_x-10,center_y+10,center_z,1])

p5 = vectorToMatrix([center_x-10,center_y-10,center_z+20,1])
p6 = vectorToMatrix([center_x+10,center_y-10,center_z+20,1])
p7 = vectorToMatrix([center_x+10,center_y+10,center_z+20,1])
p8 = vectorToMatrix([center_x-10,center_y+10,center_z+20,1])


# drawVectorPoint(p1)
# drawVectorPoint(p2)
# drawVectorPoint(p3)
# drawVectorPoint(p4)
# drawVectorPoint(p5)
# drawVectorPoint(p6)
# drawVectorPoint(p7)
# drawVectorPoint(p8)
# draw_line(p1,p2)
# draw_line(p2,p3)
# draw_line(p3,p4)
# draw_line(p4,p1)
# draw_line(p5,p6)
# draw_line(p6,p7)
# draw_line(p7,p8)
# draw_line(p8,p5)
#
# draw_line(p1,p5)
# draw_line(p2,p6)
# draw_line(p3,p7)
# draw_line(p4,p8)

update_screen()
time.sleep(0.5)
for angle in range(0,-360,-1):
    time.sleep(0.05)

    # drawVectorPoint(p1,delete=True)
    # drawVectorPoint(p2,delete=True)
    # drawVectorPoint(p3,delete=True)
    # drawVectorPoint(p4,delete=True)

    draw_line(p1,p2,delete=True)
    draw_line(p2,p3,delete=True)
    draw_line(p3,p4,delete=True)
    draw_line(p4,p1,delete=True)
    draw_line(p5,p6,delete=True)
    draw_line(p6,p7,delete=True)
    draw_line(p7,p8,delete=True)
    draw_line(p8,p5,delete=True)
    draw_line(p1,p5,delete=True)
    draw_line(p2,p6,delete=True)
    draw_line(p3,p7,delete=True)
    draw_line(p4,p8,delete=True)

    update_screen()
    p1 = rotate_x(origin,p1,0.1)
    p2 = rotate_x(origin,p2,0.1)
    p3 = rotate_x(origin,p3,0.1)
    p4 = rotate_x(origin,p4,0.1)
    p5 = rotate_x(origin,p5,0.1)
    p6 = rotate_x(origin,p6,0.1)
    p7 = rotate_x(origin,p7,0.1)
    p8 = rotate_x(origin,p8,0.1)

    p1 = rotate_y(origin,p1,0.1)
    p2 = rotate_y(origin,p2,0.1)
    p3 = rotate_y(origin,p3,0.1)
    p4 = rotate_y(origin,p4,0.1)
    p5 = rotate_y(origin,p5,0.1)
    p6 = rotate_y(origin,p6,0.1)
    p7 = rotate_y(origin,p7,0.1)
    p8 = rotate_y(origin,p8,0.1)

    p1 = rotate_z(origin,p1,0.1)
    p2 = rotate_z(origin,p2,0.1)
    p3 = rotate_z(origin,p3,0.1)
    p4 = rotate_z(origin,p4,0.1)
    p5 = rotate_z(origin,p5,0.1)
    p6 = rotate_z(origin,p6,0.1)
    p7 = rotate_z(origin,p7,0.1)
    p8 = rotate_z(origin,p8,0.1)

    # drawVectorPoint(p1)
    # drawVectorPoint(p2)
    # drawVectorPoint(p3)
    # drawVectorPoint(p4)

    draw_line(p1,p2,color=(0,255,255))
    draw_line(p2,p3,color=(255,0,255))
    draw_line(p3,p4,color=(255,255,0))
    draw_line(p4,p1,color=(0,255,0))
    draw_line(p5,p6,color=(0,0,255))
    draw_line(p6,p7,color=(255,0,0))
    draw_line(p7,p8,color=(255,255,255))
    draw_line(p8,p5,color=(255,255,255))

    draw_line(p1,p5,color=(255,255,255))
    draw_line(p2,p6,color=(255,255,255))
    draw_line(p3,p7,color=(255,255,255))
    draw_line(p4,p8,color=(255,255,255))

    update_screen()
    # print(angle)
    # print(p1)
    # print(p2)
    # print(p3)
    # print(p4)
exit()
