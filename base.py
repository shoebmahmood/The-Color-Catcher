from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_WIDTH = 800
W_HEIGHT = 600

#predefined set of bright colors for convenience
color_set = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1,1,1)]


def write_pixel(x, y, color): #use color as a tuple, e.g. color = (1,1,1)
    glPointSize(2)
    glBegin(GL_POINTS)
    glColor3fv(color)
    glVertex2f(x,y)
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
        x1, y1, x2, y2 = convert_point_to_zone_0(x1, y1, zone)[0], convert_point_to_zone_0(x1, y1, zone)[1], convert_point_to_zone_0(x2, y2, zone)[0], convert_point_to_zone_0(x2, y2, zone)[1]
        dx = x2 - x1
        dy = y2 - y1

    d = (2 * dy) - dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy - dx)
    x, y = x1, y1

    while x <= x2 and y <= y2:
        write_pixel(revert_point_to_prev_zone(x, y, zone)[0], revert_point_to_prev_zone(x, y, zone)[1],color)
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

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and # x_min_1 < x_max_2
                self.x + self.w > other.x  and # x_max_1 > m_min_2
                self.y < other.y + other.h and # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2

def catcher(x, y, color):
    blx, bly = x, y
    brx, bry = x+100, y
    ulx, uly = x, y+20
    urx, ury = x+100, y+20
    draw_line(ulx, uly, urx, ury, color)
    draw_line(ulx, uly, blx, bly, color)
    draw_line(urx, ury, brx, bry, color)
    draw_line(blx, bly, brx, bry, color)





def initialize():
    global W_WIDTH, W_HEIGHT
    glViewport(0, 0, W_WIDTH, W_HEIGHT)   
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()             
    glOrtho(0.0, W_WIDTH, 0.0, W_HEIGHT, 0.0, 1.0)  
    glMatrixMode (GL_MODELVIEW)  
    glLoadIdentity()


catcher_x = 350
catchbox = AABB(catcher_x, 10, 100, 20)
def special_key_listener(key, x, y):
    global catcher_x, catchbox

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
    
    glutPostRedisplay()
        

ball_color = random.choice(color_set)
spawnx = [] #set of x values for the ball
for i in range(100):
    spawnx.append(random.randint(30, 770))

ball_x = random.choice(spawnx)
ball_y = 630
ballbox = AABB(ball_x-10, ball_y-10, 20, 20)
def animate():
    global ball_x, ball_y, ball_color, ballbox
    ball_y -= 1
    ballbox.y -= 1

    if ball_y <= 0:
        ball_color = random.choice(color_set)
        ball_x = random.choice(spawnx)
        ball_y = 630
        mid_circle(ball_x, ball_y, 10, ball_color)
    glutPostRedisplay()






catcher_color = random.choice(color_set)

def display():
    global color_set, catcher_x, catcher_color, ball_x, ball_y, ball_color, ballbox
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    catcher(catcher_x, 10, catcher_color)
    mid_circle(ball_x, ball_y, 10, ball_color)

    if ballbox.collides_with(catchbox):
        glutLeaveMainLoop()
        print("Collided")

    
        

    
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_RGBA)

window = glutCreateWindow(b"EWWW")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(special_key_listener)


initialize()
glutMainLoop()
