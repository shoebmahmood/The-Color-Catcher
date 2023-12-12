from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from time import time
import time

W_WIDTH = 800
W_HEIGHT = 600
falling_diamonds = []
falling_squares = [] 
score=0
def write_pixel(x, y, color):  # use color as a tuple, e.g. color = (1,1,1)
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3fv(color)
    glVertex2f(x, y)
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6
    return zone

def convert_point_to_zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def revert_point_to_prev_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    else:
        return x, -y

def draw_line(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    zone = find_zone(x1, y1, x2, y2)

    if zone != 0:
        x1, y1, x2, y2 = convert_point_to_zone_0(x1, y1, zone)[0], convert_point_to_zone_0(x1, y1, zone)[1], \
                         convert_point_to_zone_0(x2, y2, zone)[0], convert_point_to_zone_0(x2, y2, zone)[1]
        dx = x2 - x1
        dy = y2 - y1

    d = (2 * dy) - dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy - dx)
    x, y = x1, y1

    while x <= x2 and y <= y2:
        write_pixel(revert_point_to_prev_zone(x, y, zone)[0], revert_point_to_prev_zone(x, y, zone)[1], color)
        if d < 0:
            d += inc_e
            x += 1
        else:
            d += inc_ne
            x += 1
            y += 1

def circ_point(x, y, cx, cy):
    glVertex2f(x + cx, y + cy)
    glVertex2f(y + cx, x + cy)

    glVertex2f(y + cx, -x + cy)
    glVertex2f(x + cx, -y + cy)

    glVertex2f(-x + cx, -y + cy)
    glVertex2f(-y + cx, -x + cy)

    glVertex2f(-y + cx, x + cy)
    glVertex2f(-x + cx, y + cy)

def mid_circle(cx, cy, radius, color):
    d = 1 - radius
    x = 0
    y = radius

    glColor3f(color[0], color[1], color[2])
    glPointSize(2)
    glBegin(GL_POINTS)
    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y = y - 1
        x = x + 1
        circ_point(x, y, cx, cy)
    glEnd()

def draw_score():
    global score  

    # Define the position for the score display
    x = 10
    y = 570

    # Draw each digit of the score as a line
    if score == 0:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            
    if score == 1:
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            
    if score == 2:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 3:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 4:
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 5:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 6:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 7:
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
    if score == 8:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 9:
            draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
            
            draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
            draw_line(x, y+10, x, y+20, (1, 1, 1))#top left
            draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
            draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
            draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle
    if score == 10:
        
        draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
       
        draw_line(x + 20, y, x + 30, y, (1, 1, 1))  # bottom
        draw_line(x + 20, y, x + 20, y + 20, (1, 1, 1))  # leftmost line
        draw_line(x + 30, y, x + 30, y + 20, (1, 1, 1))  # rightmost line
        draw_line(x + 20, y + 20, x + 30, y + 20, (1, 1, 1))  # top
    if score == 11:
        draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right

        draw_line(x+20, y, x+20, y+20, (1, 1, 1))  # vertical line
        draw_line(x + 10, y, x + 10, y + 20, (1, 1, 1))  # leftmost line
    if score == 12:
        draw_line(x+10,  y, x+10, y+10, (1, 1, 1))  # bottom right
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))  # top right

        draw_line(x + 20, y, x + 30, y, (1, 1, 1))  # bottom
        draw_line(x + 20, y, x + 20, y + 10, (1, 1, 1))  # bottom left
        draw_line(x + 30, y + 10, x + 30, y + 20, (1, 1, 1))  # top right
        draw_line(x + 20, y + 20, x + 30, y + 20, (1, 1, 1))  # top
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
    if score == 13:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x + 20, y, x + 30, y, (1, 1, 1))  # bottom
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
        draw_line(x + 20, y + 20, x + 30, y + 20, (1, 1, 1))  # top
        draw_line(x + 30, y, x + 30, y + 20, (1, 1, 1))  # right
    if score == 14:
        # Draw the "1"
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x + 30, y, x + 30, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 20, y + 10, x + 20, y + 20, (1, 1, 1))  # top left
        draw_line(x + 30, y + 10, x + 30, y + 20, (1, 1, 1))  # top right
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
    if score == 15:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left 
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 16:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 17:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
    if score == 18:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    
    if score == 19:
        draw_line(x + 10, y, x + 10, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 10, y + 10, x + 10, y + 20, (1, 1, 1))  # top right

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 20:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
    if score == 21:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x+20, y+20, (1, 1, 1))  # vertical line
       
    if score == 22:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x + 20, y, x + 30, y, (1, 1, 1))  # bottom
        draw_line(x + 20, y, x + 20, y + 10, (1, 1, 1))  # bottom left
        draw_line(x + 30, y + 10, x + 30, y + 20, (1, 1, 1))  # top right
        draw_line(x + 20, y + 20, x + 30, y + 20, (1, 1, 1))  # top
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
    if score == 23:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x + 20, y, x + 30, y, (1, 1, 1))  # bottom
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
        draw_line(x + 20, y + 20, x + 30, y + 20, (1, 1, 1))  # top
        draw_line(x + 30, y, x + 30, y + 20, (1, 1, 1))  # right
    if score == 24:
        # Draw the "1"
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x + 30, y, x + 30, y + 10, (1, 1, 1))  # bottom right
        draw_line(x + 20, y + 10, x + 20, y + 20, (1, 1, 1))  # top left
        draw_line(x + 30, y + 10, x + 30, y + 20, (1, 1, 1))  # top right
        draw_line(x + 20, y + 10, x + 30, y + 10, (1, 1, 1))  # middle
    if score == 25:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left 
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 26:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 27:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
    if score == 28:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    
    if score == 29:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x, y, x, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        draw_line(x+20, y+10, x+30, y+10, (1, 1, 1))#middle
    if score == 30:
        draw_line(x, y, x + 10, y, (1, 1, 1)) #bottom
        draw_line(x+10,  y, x+10, y+10, (1, 1, 1))#bottom right
        draw_line(x+10, y+10, x+10, y+20, (1, 1, 1))#top right
        draw_line(x, y+20, x+10, y+20, (1, 1, 1))#top
        draw_line(x, y+10, x+10, y+10, (1, 1, 1))#middle

        draw_line(x+20, y, x + 30, y, (1, 1, 1)) #bottom
        draw_line(x+20, y, x+20, y + 10, (1, 1, 1)) #bottom left
        draw_line(x+30,  y, x+30, y+10, (1, 1, 1))#bottom right
        draw_line(x+20, y+10, x+20, y+20, (1, 1, 1))#top left
        draw_line(x+30, y+10, x+30, y+20, (1, 1, 1))#top right
        draw_line(x+20, y+20, x+30, y+20, (1, 1, 1))#top
        





        




class AABB:
    x = 0
    y = 0
    w = 0
    h = 0
    instances = {} 

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.instance_id = id(self)
        AABB.instances[self.instance_id] = self  # Store the instance in the dictionary

    def increase_width(self, amount):
        self.w += amount

    def collides_with(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)


    def collides_with_bullet(self, bullet_x, bullet_y):
    # Check for collision between the AABB and the bullet
        return (self.x < bullet_x < self.x + self.w and
                self.y < bullet_y < self.y + self.h)
    
    def check_collision_with_catcher(x1, y1, x2, y2, catcher_box):
        # Check for collision between the line and the catcher
        line_box = AABB(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        return line_box.collides_with(catcher_box)

    def collides_with_catcher(self, x, y, catcher_box):
        diamond_center_x = x
        diamond_center_y = y

        catcher_top = catcher_box.y + catcher_box.h
        catcher_bottom = catcher_box.y
        catcher_left = catcher_box.x
        catcher_right = catcher_box.x + catcher_box.w

        # Check if any point of the diamond is close enough to the catcher's bounds
        diamond_points = [
            (diamond_center_x, diamond_center_y -20),  # Top point
            (diamond_center_x - 20, diamond_center_y),  # Right point
            (diamond_center_x, diamond_center_y - 20),  # Bottom point
            (diamond_center_x - 20, diamond_center_y),  # Left point
        ]

        for point in diamond_points:
            x, y = point
            if catcher_left <= x <= catcher_right and catcher_bottom <= y <= catcher_top:
                return True

        return False
    def bullet_collision_handler():
        global ball_color, falling_diamonds, bullet_active, ball_x, ball_y

        if ballbox.collides_with_bullet(bullet_x, bullet_y):
            if ball_color != catcher_color:
                # Generate a random number between 0 and 100
                rand_num = random.randint(0, 100)

                if rand_num % 2 == 0:
                    # Draw a falling diamond at the location where the ball disappeared
                    diamond(ball_x - 10, ball_y - 10, ball_color, ball_y, falling_diamonds)
                else:
                    # Draw a falling square at the location where the ball disappeared
                    draw_square(ball_x - 10, ball_y - 10, ball_color)

                # Reset the ball's position and color
                ball_color = random.choice(color_set)
                ball_x = random.choice(spawnx)
                ball_y = 630
                ballbox.x = ball_x - 10
                ballbox.y = ball_y - 10

                # Deactivate the bullet
                bullet_active = False
            else:
                bullet_active = False
                print("Game Over - Bullet collided with a ball of the same color as the catcher!")
                game_over = True

# Predefined set of bright colors for convenience
color_set = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]

def catcher(x, y, width, color):
    blx, bly = x, y
    brx, bry = x + width, y
    ulx, uly = x, y + 20
    urx, ury = x + width, y + 20
    draw_line(ulx, uly, urx, ury, color)
    draw_line(ulx, uly, blx, bly, color)
    draw_line(urx, ury, brx, bry, color)
    draw_line(blx, bly, brx, bry, color)

def draw_diamond(x, y, color):
    cx, cy = x + 50, y + 10  # Update the center of the diamond based on ball_y
    size = 20  # Adjust the size of the diamond as needed

    draw_line(cx, cy + size, cx + size / 2, cy, color)
    draw_line(cx + size / 2, cy, cx, cy - size, color)
    draw_line(cx, cy - size, cx - size / 2, cy, color)
    draw_line(cx - size / 2, cy, cx, cy + size, color)

def falling_diamond(x, y, color, falling_diamonds):
    draw_diamond(x, y, color)

    falling_diamonds.append({
        'x': x,
        'y': y,
        'color': color,
    })

def update_falling_diamonds(falling_diamonds):
    global catcher_caught_square, original_catcher_width, catcher_caught_square_this_cycle

    for diamond in falling_diamonds:
        draw_diamond(diamond['x'], diamond['y'], diamond['color'])

        # Check for collision with the catcher
        if catchbox.collides_with(AABB(diamond['x'] - 20, diamond['y'], 40, 20)) and not catcher_caught_square_this_cycle:
            print("Catcher caught a falling diamond!")
            catchbox.increase_width(20)  # Increase the width permanently
            original_catcher_width = catchbox.w  # Update the original catcher width
            catcher_caught_square_this_cycle = True  # Set the flag to True

        diamond['y'] -= square_speed

        # Reset the flag when the diamond is no longer colliding with the catcher
        if not catchbox.collides_with(AABB(diamond['x'] - 20, diamond['y'], 40, 20)):
            catcher_caught_square_this_cycle = False

    # Remove diamonds that have fallen below the lower boundary
    falling_diamonds[:] = [diamond for diamond in falling_diamonds if diamond['y'] >= 0]



def draw_square(x, y, color):
    blx, bly = x, y
    brx, bry = x + 20, y
    ulx, uly = x, y + 20
    urx, ury = x + 20, y + 20
    draw_line(ulx, uly, urx, ury, color)
    draw_line(ulx, uly, blx, bly, color)
    draw_line(urx, ury, brx, bry, color)
    draw_line(blx, bly, brx, bry, color)

square_speed = 1  # You can adjust the speed of the square falling
def falling_square(x, y, color, falling_squares):
    draw_square(x, y, color)

    falling_squares.append({
        'x': x,
        'y': y,
        'color': color,
    })
catcher_caught_square_this_cycle = False

def update_falling_squares(falling_squares):
    global catcher_caught_square, original_catcher_width, catcher_caught_square_this_cycle

    for square in falling_squares:
        draw_square(square['x'], square['y'], square['color'])

        # Check for collision with the catcher
        if catchbox.collides_with(AABB(square['x'], square['y'], 20, 20)) and not catcher_caught_square_this_cycle:
            print("Catcher caught a power-up!")
            print('increase width')
            catchbox.increase_width(20)  # Increase the width permanently
            original_catcher_width = catchbox.w  # Update the original catcher width
            catcher_caught_square_this_cycle = True  # Set the flag to True

        square['y'] -= square_speed

        # Reset the flag when the square is no longer colliding with the catcher
        if not catchbox.collides_with(AABB(square['x'], square['y'], 20, 20)):
            catcher_caught_square_this_cycle = False

    # Remove squares that have fallen below the lower boundary
    falling_squares[:] = [square for square in falling_squares if square['y'] >= 0]



#------------------------------------------------------------------------------------------------------------------------------#





game_over = False



catcher_x = 350 # Initial position of the catcher
catchbox = AABB(catcher_x, 10, 100, 20) # AABB for the catcher
catcher_color = random.choice(color_set) # Initial color of the catcher
original_catcher_width = 60
catcher_caught_square = False


bullet_active = False
bullet_x = 0
bullet_y = 0
bullet_color = (1, 1, 1)
bullet_duration = 0.1  # in seconds
last_shoot_time = time.time()


ball_color = random.choice(color_set)
spawnx = []  # set of x values for the ball
for i in range(100):
    spawnx.append(random.randint(50, 750))

ball_x = random.choice(spawnx)
ball_y = 630
ballbox = AABB(ball_x - 10, ball_y - 10, 20, 20)


def update_bullet():
    global bullet_active, bullet_y, bullet_duration, last_shoot_time

    if bullet_active:
        bullet_y += 5

    if bullet_y > W_HEIGHT:
        bullet_active = False
        last_shoot_time = time.time()


def shoot_bullet():
    global bullet_active, bullet_x, bullet_y, catcher_x, catchbox

    bullet_active = True

    # Calculate the initial position of the bullet based on the updated catcher width
    bullet_x = catcher_x + catchbox.w / 2
    bullet_y = 30

def restart_game():
    global score, falling_diamonds, falling_squares
    score = 0
    falling_diamonds = []
    falling_squares = []
    global game_over
    game_over=False
    main()
    display()
    animate()
    display.bullet_collision_handler()
    display.diamond_collision_handler()
    
    
def keyboard_listener(key, x, y):
    global catcher_color, catchbox

    if key == b' ':
        # Change the catcher color randomly to another color
        restart_game()

        # If catcher caught a square and its width increased, update the AABB
        


def special_key_listener(key, x, y):
    global catcher_x, catchbox, original_catcher_width

    if key == GLUT_KEY_LEFT:
        if catcher_x == 10:
            pass
        else:
            catcher_x -= 20
            catchbox.x -= 20
    elif key == GLUT_KEY_RIGHT:
        if catcher_x == 690:
            pass
        else:
            catcher_x += 20
            catchbox.x += 20

    # If catcher caught a square and its width increased, update the AABB

    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global bullet_active, last_shoot_time
    global catcher_color, catchbox

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Change the catcher color randomly to another color
        catcher_color = random.choice([color for color in color_set if color != catcher_color])

        # If catcher caught a square and its width increased, update the AABB
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Shoot the bullet
        if not bullet_active:
            shoot_bullet()
            last_shoot_time = time.time()

dflag = False
sFlag = False

def animate():
    global ball_x, ball_y, ball_color, ballbox, game_over, dflag, sFlag

    if not game_over:
        ball_y -= 1
        ballbox.y -= 1

        if ball_y <= 0:
            print("Game Over - Ball went beyond the boundary!")
            game_over = True

        glutPostRedisplay()

def display():
    global game_over, catcher_color, ball_color, catcher_x, catcher_color, bullet_active, bullet_x, bullet_y, bullet_color, ball_x, ball_y, dflag, sFlag

    global falling_diamonds, falling_squares, original_catcher_width, catcher_caught_square  # Add the flag to the global variables

    def bullet_collision_handler():
        global ball_color, falling_diamonds, falling_squares, bullet_active, ball_x, ball_y, game_over

        if ballbox.collides_with_bullet(bullet_x, bullet_y):
            if ball_color != catcher_color:
                global score
                score += 1
                # Generate a random number between 1 and 100
                rand_num = random.randint(1, 100)

                if 1 <= rand_num <= 30:  # Adjust the threshold as needed
                    falling_diamond(ball_x - 10, ball_y - 10, ball_color, falling_diamonds)
                elif 30 < rand_num <= 60  :
                    falling_square(ball_x - 10, ball_y - 10, ball_color, falling_squares)

                # Reset the ball's position and color
                ball_color = random.choice(color_set)
                ball_x = random.choice(spawnx)
                ball_y = 630
                ballbox.x = ball_x - 10
                ballbox.y = ball_y - 10

                # Deactivate the bullet
                bullet_active = False
            else:
                bullet_active = False
                print("Game Over - Bullet collided with a ball of the same color as the catcher!")
                game_over = True

    def diamond_collision_handler():
        global game_over

        for falling_diamond in falling_diamonds:
            # Check for collision with the catcher
            if catchbox.collides_with(AABB(falling_diamond['x'] - 20, falling_diamond['y'], 40, 20)):
                print("Game Over - Catcher caught a falling bug!")
                game_over = True

        # Remove diamonds that have fallen below the lower boundary
        falling_diamonds[:] = [diamond for diamond in falling_diamonds if diamond['y'] >= 0]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    catcher(catcher_x, 10, catchbox.w, catcher_color)

    update_bullet()

    if not game_over:
        if bullet_active:
            draw_line(bullet_x, bullet_y, bullet_x, bullet_y + 10, bullet_color)
            bullet_collision_handler()

        mid_circle(ball_x, ball_y, 10, ball_color)

        if ball_y < 0:
            if ball_color == catcher_color:
                catcher_color = random.choice([color for color in color_set if color != catcher_color])
            else:
                print("Game Over - Ball went beyond the boundary!")
                game_over = True

        if catchbox.collides_with_catcher(ball_x, ball_y, catchbox):
            if ball_color == catcher_color:
                catcher_color = random.choice([color for color in color_set if color != catcher_color])
                ball_color = random.choice(color_set)
                ball_x = random.choice(spawnx)
                ball_y = 630
                ballbox.x = ball_x - 10
                ballbox.y = ball_y - 10
                global score
                score += 1
                
            else:
                print("Game Over - Catcher caught a ball of different color!")
                game_over = True

        update_falling_diamonds(falling_diamonds)
        update_falling_squares(falling_squares)
        draw_score()
        diamond_collision_handler()  # Check for collision with falling diamonds
         

    glutSwapBuffers()



# Rest of the code remains unchanged.

def main():
    global original_catcher_width  # Add this line to make the variable global

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(W_WIDTH, W_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catcher Game")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_click)  # Register the mouse click function

    original_catcher_width = 60  # Set the initial value for the original catcher width
    catchbox = AABB(catcher_x, 10, original_catcher_width, 10)  # Update the catcher's AABB with the original width

    glOrtho(0, W_WIDTH, 0, W_HEIGHT, -1, 1)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glutMainLoop()

if __name__ == "__main__":
    main()