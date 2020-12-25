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
        self.zbuffer=0

# PARAMETERS(make this class-based later....)
bkg=" "
bkg_color="#333333"
dot='o'
size_x,size_y,size_z = 80,50,80
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = int(size_z / 2)
origin=[center_x,center_y,center_z,1]
OLD_DEBUG=None
DEBUG=None

#create the grid
grid = []
for y in range(size_y):
    row=[]
    for x in range(size_x):
        row.append(cell(x,y))
    grid.append(row)

def updateScreen():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            if cell.hasChanged:
                cell.hasChanged=False
                if cell.color is not None:
                    moveCursor(row,col)
                    print(color(f"{cell.tile}",cell.color))

    global DEBUG
    DEBUG=f"cell {center_x},{center_y} zbuffer is {grid[center_y][center_x].zbuffer}"
    cell = grid[center_y][center_x]
    cell.color=(200,200,200)
    moveCursor(center_y,center_x)
    print(color(f"{cell.tile}",cell.color))

def eraseLine(p1,p2):
    drawLine(p1,p2,delete=True)

def shader(color,point,max_z=0):
    #scale color based on Z value...
    global DEBUG
    color2 = list(color[:])

    #normalize Z values to 0-255
    if max_z !=0:
        scaler = (point[2]) / (max_z)
    else:
        scaler = 1

    # r = color[0]  * scaler
    # g = color[1]  * scaler
    # b = color[2]  * scaler

    color2[0] = int(color[0] * scaler)
    color2[1] = int(color[1] * scaler)
    color2[2] = int(color[2] * scaler)

    if color2[0] > 255:color2[0]=255
    if color2[1] > 255:color2[1]=255
    if color2[2] > 255:color2[2]=255
    return color2

def drawLine(p1,p2,color=(255,255,255),delete=False):
    points = calculateLine(p1,p2)
    z1 = int(p1[2]+0.5)
    z2 = int(p2[2]+0.5)

    for p in points:
        cell = grid[p[1]][p[0]]
        cell.tile = dot if delete==False else bkg
        if z1 > z2:
            color = shader(color,p1) if delete==False else color
        else:
            color = shader(color,p2) if delete==False else color
        cell.color = color  if delete==False else bkg_color
        if z1 < cell.zbuffer:
            cell.zbuffer = z1
            cell.hasChanged=True
        if z2 < cell.zbuffer:
            cell.zbuffer = z2
            cell.hasChanged=True

def calculateLine(p1,p2):
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
    x,y,z=int(point[0]+0.5),int(point[1]+0.5),int(point[2]+0.5)
    cell = grid[y][x]
    cell.tile = dot if delete==False else bkg
    cell.color = color  if delete==False else bkg_color

    if z > cell.zbuffer or delete==True:
        cell.hasChanged=True
        cell.zbuffer = z

def vectorToMatrix(vector):
    return [[p] for p in vector]

def matrixToVector(matrix):
    return [element[0] for element in matrix]

def translatePoint(pivot,point):
    tx,ty,tz = pivot[0],pivot[1],pivot[2]
    translation_matrix = [
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0]
    ]
    return matrixMultiply(translation_matrix,point)

def matrixMultiply(a, b):
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

def rotateX(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    #translate
    point = translatePoint(inverted_pivot,point)
    xrot=[
        [1.0,   0.0,    0.0,    0.0],
        [0.0,   cos,    -sin,   0.0],
        [0.0,   sin,    cos,    0.0],
        [0.0,   0.0,    0.0,    1.0]
        ]
    #rotate
    point = matrixMultiply(xrot,point)
    #translate back
    point = translatePoint(pivot,point)

    return point

def rotateY(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    #translate
    point = translatePoint(inverted_pivot,point)
    yrot=[
        [cos,   0.0,    sin,    0.0],
        [0.0,   1.0,    0.0,    0.0],
        [-sin,  0.0,    cos,    0.0],
        [0.0,   0.0,    0.0,    1.0]
        ]
    #rotate
    point = matrixMultiply(yrot,point)
    #translate back
    point = translatePoint(pivot,point)
    return point

def rotateZ(pivot,point,angle):
    rads = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    inverted_pivot = [-pivot[0],-pivot[1],-pivot[2]]
    old_point = list(point)
    #translate
    point = translatePoint(inverted_pivot,point)
    zrot=[
        [cos,   -sin,   0.0,    0.0],
        [sin,   cos,    0.0,    0.0],
        [0.0,   0.0,    1.0,    0.0],
        [0.0,   0.0,    0.0,    1.0]
        ]

    #rotate
    point = matrixMultiply(zrot,point)
    #translate back
    point = translatePoint(pivot,point)

    return point

def rotateModel(model,pivot,axis,angle):
    ''' Rotates every point in a model around the chosen pivot'''

    if WIREFRAME_ENABLED:
        eraseWireframe(model)


    if axis=='x':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotateX(pivot,p,angle)
    if axis=='y':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotateY(pivot,p,angle)
    if axis=='z':
        for i,p in enumerate(model['points']):
            model['points'][i] = rotateZ(pivot,p,angle)

    if FILL_POLYGONS:
        polyFill(model)
    if WIREFRAME_ENABLED:
        drawWireframe(model)
    updateScreen()

def eraseWireframe(model):
    for poly in model['polygons']:
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3]
        eraseLine(p1,p2)
        eraseLine(p2,p3)
        eraseLine(p3,p1)

def drawWireframe(model):
    for poly in model['polygons']:
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3]
        drawLine(p1,p2,color)
        drawLine(p2,p3,color)
        drawLine(p3,p1,color)

def printDebug():
    global DEBUG,OLD_DEBUG
    if DEBUG == OLD_DEBUG:
        time.sleep(0.01)
        return
    moveCursor(len(grid),0)
    print(' '*50)
    moveCursor(len(grid),0)
    print(DEBUG)
    OLD_DEBUG = DEBUG

def polyFill(model):
    global DEBUG
    ''' test to sort the polygons based on their Z-values
        so that we can draw them in a specific order
        This is built in a clunky way just to confirm
        the principle, it should be rebuilt later '''
    polygon_z_list=[]
    for i,poly in enumerate(model['polygons']):
        p1_z = matrixToVector(model['points'][poly[0]])[2]
        p2_z = matrixToVector(model['points'][poly[1]])[2]
        p3_z = matrixToVector(model['points'][poly[2]])[2]
        # sum the z points
        polygon_z_list.append([i,p1_z+p2_z+p3_z])
    #sort the list from low to high
    polygon_z_list.sort(key=lambda x: x[1])


    # '''debug'''
    # for i,pz in enumerate(polygon_z_list):
    #     poly = model['polygons'][pz[0]]
    #     if poly[3] == (255,0,0):
    #         DEBUG =f"Red triangle is {i}/{len(polygon_z_list)-1} in polygon_z_list and Z value:{matrixToVector(model['points'][poly[0]])[2]}"
    # '''/debug'''

    #clear all old colored points
    for p in model['old_points']:
        drawVectorPoint(p,None,delete=True)
    # Reset old points
    model['old_points']=[]

    # Fill in polygons with color
    for pz in polygon_z_list:
    # for i in range(len(polygon_z_list)):
        poly = model['polygons'][pz[0]]
        p1 = matrixToVector(model['points'][poly[0]])
        p2 = matrixToVector(model['points'][poly[1]])
        p3 = matrixToVector(model['points'][poly[2]])
        color = poly[3]
        # calc line between two points...
        line_a_to_b = calculateLine(p1,p2)
        # calc line from each points of the above calculated line, to point3
        # and draw the lines(shading based on z_value)
        for point in line_a_to_b:
            line = calculateLine(point,p3)
            max_z = max(line, key=lambda x: x[2])[2] #extract max Z-value
            for p in line:
                if SHADER_ENABLED:
                    shaded_color = shader(color,p,max_z)
                else:
                    shaded_color = color
                drawVectorPoint(p,shaded_color)
                model['old_points'].append(p)
if __name__ == '__main__':
    DEBUG='start'
    FILL_POLYGONS=True
    SHADER_ENABLED=False
    WIREFRAME_ENABLED=False
    # model = models.cube
    # polyFill(model)

    # updateScreen()
    models =[models.cube]
    
    while True:
        if keyboard.is_pressed('w'):
            WIREFRAME_ENABLED = not(WIREFRAME_ENABLED)
        if keyboard.is_pressed('s'):
            SHADER_ENABLED = not(SHADER_ENABLED)
        if keyboard.is_pressed('p'):
            FILL_POLYGONS = not(FILL_POLYGONS)
        if keyboard.is_pressed('right'):
            for model in models:
                rotateModel(model,origin,'y',0.1)
        if keyboard.is_pressed('left'):
            for model in models:
                rotateModel(model,origin,'y',-0.1)
        if keyboard.is_pressed('up'):
            for model in models:
                rotateModel(model,origin,'x',0.1)
        if keyboard.is_pressed('down'):
            for model in models:
                rotateModel(model,origin,'x',-0.1)
        if keyboard.is_pressed('z'):
            for model in models:
                rotateModel(model,origin,'z',0.1)
        if keyboard.is_pressed('x'):
            for model in models:
                rotateModel(model,origin,'z',-0.1)
        printDebug()
