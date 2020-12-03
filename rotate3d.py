# @Date:   2020-11-29T20:15:25+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: rotate3d.py
# @Last modified time: 2020-12-03T22:53:26+01:00



import os
import sys
import time
import math
import models
import random
import keyboard
from colors import color
''' this is the ansicolors module ^^^ '''

import ctypes
from ctypes import c_long, c_ulong
gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))
os.system('')

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
dot='o'
size_x,size_y,size_z = 80,50,80
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = int(size_z / 2)
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

def shader(color,point):
    color = list(color)
    if len(color) < 1:return
    #scale color based on Z value...
    color[0] = int(color[0] * point[2][0] / 20)
    color[1] = int(color[1] * point[2][0] / 20)
    color[2] = int(color[2] * point[2][0] / 20)
    if color[0] > 255:color[0]=255
    if color[1] > 255:color[1]=255
    if color[2] > 255:color[2]=255
    # print(f"Z:{point[2]} color:{color[0]} {color[1]} {color[2]}")
    return color

def draw_line(p1,p2,color=(255,255,255),delete=False):
    try:
        x1 = int(p1[0][0]+0.5)
        y1 = int(p1[1][0]+0.5)
        z1 = int(p1[2][0]+0.5)
        x2 = int(p2[0][0]+0.5)
        y2 = int(p2[1][0]+0.5)
        z2 = int(p2[2][0]+0.5)
        dx = x2-x1
        dy = y2-y1
        dx1=abs(dx)
        dy1=abs(dy)
        px=2*dy1-dx1
        py=2*dx1-dy1

        if dy1 <= dx1:
            if dx >= 0:
                x,y,xe=x1,y1,x2
            else:
                x,y,xe=x2,y2,x1
            cell = grid[y][x]
            cell.tile = dot if delete==False else bkg
            if z1 > z2:
                color = shader(color,p1) if delete==False else color
            else:
                color = shader(color,p2) if delete==False else color
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
                if z1 > z2:
                    color = shader(color,p1) if delete==False else color
                else:
                    color = shader(color,p2) if delete==False else color
                cell.color = color if delete==False else bkg_color
                cell.hasChanged=True
        else:
            if dy >= 0:
                x,y,ye = x1,y1,y2
            else:
                x,y,ye = x2,y2,y1
            cell = grid[y][x]
            cell.tile = dot if delete==False else bkg
            if z1 > z2:
                color = shader(color,p1) if delete==False else color
            else:
                color = shader(color,p2) if delete==False else color
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
                if z1 > z2:
                    color = shader(color,p1) if delete==False else color
                else:
                    color = shader(color,p2) if delete==False else color
                cell.color = color if delete==False else bkg_color
                cell.hasChanged=True
    except IndexError as e:
        pass
        # print(f"IndexError X:{x} Y:{y}")
        # print(color,p1)

def calculate_line(p1,p2):
    ''' returns all points between two points forming a line'''
    line=[]
    x1 = int(p1[0][0]+0.5)
    y1 = int(p1[1][0]+0.5)
    x2 = int(p2[0][0]+0.5)
    y2 = int(p2[1][0]+0.5)
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
            line.append([[x],[y]])
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
                # line.append([[x],[y]])
        else:
            if dy >= 0:
                x,y,ye = x1,y1,y2
            else:
                x,y,ye = x2,y2,y1
            line.append([[x],[y]])
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
                line.append([[x],[y]])
    except IndexError:
        pass
        # print(f"X:{x} Y:{y}")
    return line

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
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0]
    ]
    return matrix_multiply(translation_matrix,point)

def matrix_multiply(a, b):
    colsA=len(a[0])
    rowsA=len(a)
    colsB=len(b[0])
    rowsB=len(b)
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
        [1.0,   0.0,    0.0,    0.0],
        [0.0,   cos,    -sin,   0.0],
        [0.0,   sin,    cos,    0.0],
        [0.0,   0.0,    0.0,    1.0]
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
        [cos,   0.0,    sin,    0.0],
        [0.0,   1.0,    0.0,    0.0],
        [-sin,  0.0,    cos,    0.0],
        [0.0,   0.0,    0.0,    1.0]
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
        [cos,   -sin,   0.0,    0.0],
        [sin,   cos,    0.0,    0.0],
        [0.0,   0.0,    1.0,    0.0],
        [0.0,   0.0,    0.0,    1.0]
        ]

    #rotate
    point = matrix_multiply(zrot,point)
    #translate back
    point = translate_point(pivot,point)

    return point

def rotate_model(model,pivot,axis,angle):
    ''' Rotates every point in a model around the chosen pivot'''

    undraw_wireframe(model)

    if axis=='x':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_x(pivot,p,angle)
    if axis=='y':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_y(pivot,p,angle)
    if axis=='z':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotate_z(pivot,p,angle)
    draw_wireframe(model)
    update_screen()

def undraw_wireframe(model):
    for line in model['lines']:
        draw_line(
            model['points'][line[0]],
            model['points'][line[1]],
            color=None,
            delete=True
            )

def draw_wireframe(model):
    for line in model['lines']:
        p1,p2,color = line
        draw_line(
            model['points'][line[0]],
            model['points'][line[1]],
            color=line[2],)

def render_model(model):
    '''
    använd draw_line for att beräkna alla punkter mellan två punkter.
    returnera dessa och kalla den listan för line_a
    Gör likadant med en till linje(beror på ledd men börja med den nedanför i en rektangel)
    och spara undan den punktlistan i line_b.
    skap sedan nya linjer mellan dessa punkter, från punkt 1 i line_a till punkt 1 i line_b.
    färglägg dessa punkter med mer eller mindre ljus(högre värden -> 255) beroende på Z-pos.
    '''
    # first lets calc the lines between a and b
    line_a=calculate_line(model['points'][0], model['points'][1])
    line_b=calculate_line(model['points'][2], model['points'][3])
    # then lets calc and append an interpolated z value between the diagonal points points[0] and points[2]
    # the [2] means Z-value
    if model['points'][0][2] > model['points'][2][2]:
        avg_z = int((model['points'][0][2][0] - model['points'][2][2][0]) / len(line_a))
        for i,p in enumerate(line_a):
            p.append([avg_z*i])
        for i,p in enumerate(line_b):
            p.append([avg_z*i])
    else:
        avg_z = int((model['points'][2][2][0] - model['points'][0][2][0]) / len(line_a))
        for i,p in enumerate(line_a):
            p.append([avg_z*i])
        for i,p in enumerate(line_b):
            p.append([avg_z*i])
    for line in line_a:
        print(line)
    a=input()
    # line_c=calculate_line(model['points'][0], model['points'][4])
    # line_d=calculate_line(model['points'][1], model['points'][5])

    if len(line_a) > len(line_b):
        for p in range(len(line_a)):
            draw_line(line_a[p-1],line_b[p],color=(0,255,50))
    else:
        for p in range(len(line_b)):
            draw_line(line_a[p],line_b[p-1],color=(0,255,50))

    # if len(line_c) > len(line_d):
    #     for p in range(len(line_c)):
    #         draw_line(line_c[p-1],line_d[p-1],color=(255,150,255))
    # else:
    #     for p in range(len(line_d)):
    #         draw_line(line_c[p-1],line_d[p-1],color=(255,150,255))

models =[models.cube,models.tree]
# model = models.cube
while True:

    if keyboard.is_pressed('right'):
        for model in models:
            rotate_model(model,origin,'y',0.1)
    if keyboard.is_pressed('left'):
        for model in models:
            rotate_model(model,origin,'y',-0.1)
    if keyboard.is_pressed('up'):
        for model in models:
            rotate_model(model,origin,'x',0.1)
    if keyboard.is_pressed('down'):
        for model in models:
            rotate_model(model,origin,'x',-0.1)
    if keyboard.is_pressed('z'):
        for model in models:
            rotate_model(model,origin,'z',0.1)
    if keyboard.is_pressed('x'):
        for model in models:
            rotate_model(model,origin,'z',-0.1)
