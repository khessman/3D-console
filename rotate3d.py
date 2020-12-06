# @Date:   2020-11-29T20:15:25+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: rotate3d.py
# @Last modified time: 2020-12-04T13:13:11+01:00



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

def shader(color,point,max_z=0):
    #scale color based on Z value...
    global DEBUG
    color2 = list(color[:])

    #normalize Z values to 0-255
    if max_z !=0:
        scaler = (point[2]) / (max_z)
    else:
        scaler = 1


    r = color[0]  * scaler
    g = color[1]  * scaler
    b = color[2]  * scaler

    color2[0] = int(color[0] * scaler)
    color2[1] = int(color[1] * scaler)
    color2[2] = int(color[2] * scaler)

    if color2[0] > 255:color2[0]=255
    if color2[1] > 255:color2[1]=255
    if color2[2] > 255:color2[2]=255
    return color2

def draw_line(p1,p2,color=(255,255,255),delete=False):
    try:
        x1 = int(p1[0]+0.5)
        y1 = int(p1[1]+0.5)
        z1 = int(p1[2]+0.5)
        x2 = int(p2[0]+0.5)
        y2 = int(p2[1]+0.5)
        z2 = int(p2[2]+0.5)
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
    global DEBUG
    ''' returns all points between two points forming a line'''
    line=[]
    x1 = int(p1[0]+0.5)
    x2 = int(p2[0]+0.5)
    y1 = int(p1[1]+0.5)
    y2 = int(p2[1]+0.5)
    z1 = int(p1[2]+0.5)
    z2 = int(p2[2]+0.5)


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
            line.append([x,y])
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
                line.append([x,y])
        else:
            if dy >= 0:
                x,y,ye = x1,y1,y2
            else:
                x,y,ye = x2,y2,y1
            line.append([x,y])
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
                line.append([x,y])
    except IndexError:
        pass
    ''' Adding a interpolated Z depth value between points '''
    depth = (abs(z2-z1) / len(line))
    for i,l in enumerate(line):
        l.append((depth)*i)
    return line

def drawVectorPoint(point,color,delete=False):
    x,y=int(point[0]+0.5),int(point[1]+0.5)
    cell = grid[y][x]
    cell.tile = dot if delete==False else bkg
    cell.color = color  if delete==False else bkg_color
    cell.hasChanged=True

def vectorToMatrix(vector):
    return [[p] for p in vector]

def matrixToVector(matrix):
    return [element[0] for element in matrix]

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

    if RENDER_MODE == 'polygons':
        poly_fill(model)
    draw_wireframe(model)
    update_screen()

def undraw_wireframe(model):
    for poly in model['polygons']:
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3]
        draw_line(p1,p2,color,delete=True)
        draw_line(p2,p3,color,delete=True)

def draw_wireframe(model):
    for poly in model['polygons']:
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3]
        draw_line(p1,p2,color)
        draw_line(p2,p3,color)

def print_debug():
    moveCursor(len(grid),0)
    print(' '*50)
    moveCursor(len(grid),0)
    print(DEBUG)

def poly_fill(model):
    global DEBUG
    # ''' test to sort the polygons based on their Z-values
    #     so that we can draw them in a specific order
    #     This is built in a clunky way just to confirm
    #     the principle, it should be rebuilt later '''
    # polygon_z_list=[]
    # for i,poly in enumerate(model['polygons']):
    #     p1_z = matrixToVector(model['points'][poly[0]])[2]
    #     p2_z = matrixToVector(model['points'][poly[1]])[2]
    #     p3_z = matrixToVector(model['points'][poly[2]])[2]
    #     # sum the z points
    #     polygon_z_list.append([i,p1_z+p2_z+p3_z])
    # #sort the list from low to high
    # polygon_z_list.sort(key=lambda x: x[1])
    # a=input()

    ''' /test '''
    for poly in model['polygons']:
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3][:]

        line_a_to_b = calculate_line(p1,p2)
        for point in line_a_to_b:
            line = calculate_line(point,p3)
            max_z = max(line, key=lambda x: x[2])[2]
            for p in line:
                shaded_color = shader(color,p,max_z)
                drawVectorPoint(p,shaded_color)


if __name__ == '__main__':
    DEBUG='start'
    RENDER_MODE = 'polygons'
    model = models.cube
    # poly_fill(model)

    # update_screen()
    models =[models.cube]
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
        print_debug()
