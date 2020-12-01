# @Date:   2020-11-21T22:53:54+01:00
# @Email:  kalle.hessman@gmail.com
# @Filename: rotate_shape.py
# @Last modified time: 2020-11-29T20:30:13+01:00
import os
import sys
import time
import math
import numpy as np
import random
import datetime as dt
from colors import color,blue, green, white, yellow,red

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
bkg="."
bkg_color="#333333"
dot='*'
size_x,size_y = 80,50
center_x = int(size_x / 2)
center_y = int(size_y / 2)
center_z = 0
w,h=20,20
origin=[center_x,center_y,center_z,1]
#create the grid
grid = []
for y in range(size_y):
    row=[]
    for x in range(size_x):
        row.append(cell(x,y))
    grid.append(row)


def draw_XYguides():
    center_x = int(size_x / 2)
    center_y = int(size_y / 2)
    # Draw the vertical line
    for y in range(len(grid)):
        cell=grid[y][center_x]
        cell.tile = '|'
        cell.hasChanged=True
        cell.color = (255,random.randint(100,200),random.randint(0,20))
    # Draw the horizontal line
    for x in range(len(grid[0])):
        cell=grid[center_y][x]
        cell.tile = '-'
        cell.hasChanged=True
        cell.color = (255,random.randint(100,200),random.randint(0,20))

def delete_line(p1,p2):
    draw_line(p1,p2,delete=True)

# function for line generation
def draw_line(p1,p2,delete=False):
    x1,y1,x2,y2 = p1[0],p1[1],p2[0],p2[1]
    # x1,y1,x2,y2 = p1[0],p1[1],p2[0],p2[1]
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
        cell.color = (random.randint(100,200),255,random.randint(0,20))  if delete==False else bkg_color
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
            cell.color = (random.randint(100,200),255,random.randint(0,20)) if delete==False else bkg_color
            cell.hasChanged=True
    else:
        if dy >= 0:
            x,y,ye = x1,y1,y2
        else:
            x,y,ye = x2,y2,y1
        cell = grid[y][x]
        cell.tile = dot if delete==False else bkg
        cell.color = (random.randint(100,200),255,random.randint(0,20)) if delete==False else bkg_color
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
            cell.color = (random.randint(100,200),255,random.randint(0,20)) if delete==False else bkg_color
            cell.hasChanged=True

def rotate_line(pivot,p1,p2,angle):
    '''
    Pivot is tuple or list (0,0),[0,0]
    p1,p2 is tuple or list (0,0),[0,0]
    angle is int range (0 < angle < 360)

    Clockwise rotation matrix:
    [x,y]= [cos_theta,-sin_theta]
           [sin_theta,cos_theta]
    Counter-clockwise rotation matrix:
    [x,y]=[cos_theta,sin_theta]
          [-sin_theta,cos_theta]
    '''

    '''set limits'''
    max_x = len(grid[0])
    max_y = len(grid)
    rads = math.radians(angle) #converting to radians

    '''Translate from pivot to origin'''
    pivot_x = pivot[0]
    pivot_y = pivot[1]
    x_shifted1 = p1[0] - pivot_x
    y_shifted1 = p1[1] - pivot_y
    x_shifted2 = p2[0] - pivot_x
    y_shifted2 = p2[1] - pivot_y
    ''' Calculating the rotated point co-ordinates
        and shifting it back '''
    x1 = int(pivot_x + (x_shifted1 * math.cos(rads) - y_shifted1 * math.sin(rads)) + 0.5)
    y1 = int(pivot_y + (x_shifted1 * math.sin(rads) + y_shifted1 * math.cos(rads)) + 0.5)
    x2 = int(pivot_x + (x_shifted2 * math.cos(rads) - y_shifted2 * math.sin(rads)) + 0.5)
    y2 = int(pivot_y + (x_shifted2 * math.sin(rads) + y_shifted2 * math.cos(rads)) + 0.5)

    ''' Make sure we dont go outside the lists length(which will cause an indexerror) '''
    if x1 >= max_x: x1 = max_x -1
    if x1 <0:x1=0
    if x2 >= max_x: x2 = max_x -1
    if x2 <0:x2=0
    if y1 >= max_y: y1 = max_y -1
    if y1 <0:y1=0
    if y2 >= max_y: y2 = max_y -1
    if y2 <0:y2=0
    return (x1,y1),(x2,y2)

def update_screen():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            if cell.hasChanged:
                cell.hasChanged=False
                if cell.color is not None:
                    moveCursor(row,col)
                    print(color(f"{cell.tile}",cell.color))


############################################################################
#create a object
line_data=[]

line1=(center_x-int(w/2),center_y-int(h/2)),(center_x+int(w/2),center_y-int(h/2))
line2=(center_x+int(w/2),center_y-int(h/2)),(center_x+int(w/2),center_y+int(h/2))
line3=(center_x-int(w/2),center_y+int(h/2)),(center_x+int(w/2),center_y+int(h/2))
line4=(center_x-int(w/2),center_y-int(h/2)),(center_x-int(w/2),center_y+int(h/2))
line_data.append(line1)
line_data.append(line2)
line_data.append(line3)
line_data.append(line4)

while True:
    for angle in range(360):   #CCW 360 rotation
        old_lines=[]
        #Read in lines and rotate them..
        for line in line_data:
            l1 = rotate_line(origin,line[0],line[1],angle)
            draw_line(*l1)
            old_lines.append(l1)
        # Draw the lines
        update_screen()
        # And "undraw" the lines before calculating next rotated line
        for line in old_lines:
            delete_line(*line)
