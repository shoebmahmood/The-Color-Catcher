from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from time import time
import time


W_WIDTH = 800
W_HEIGHT = 600
game_over = False

# Predefined set of bright colors for convenience
color_set = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]


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


class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def collides_with(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)


    def collides_with_bullet(self, bullet_x, bullet_y):
    # Check for collision between the AABB and the bullet
        return (self.x < bullet_x < self.x + self.w and
                self.y < bullet_y < self.y + self.h)

def catcher(x, y, color):
    blx, bly = x, y
    brx, bry = x + 100, y
    ulx, uly = x, y + 20
    urx, ury = x + 100, y + 20
    draw_line(ulx, uly, urx, ury, color)
    draw_line(ulx, uly, blx, bly, color)
    draw_line(urx, ury, brx, bry, color)
    draw_line(blx, bly, brx, bry, color)

def diamond(x, y, color):
    cx, cy = x + 50, y + 10  # Center of the diamond
    size = 20  # Adjust the size of the diamond as needed

    draw_line(cx, cy + size, cx + size / 2, cy, color)
    draw_line(cx, cy - size, cx - size / 2, cy, color)
    draw_line(cx + size / 2, cy, cx, cy - size, color)
    draw_line(cx - size / 2, cy, cx, cy + size, color) 

def fall_diamond(x, y, color):
    global game_over
    dy = -3  # Adjust the falling speed
    diamond_y = y

    while diamond_y > 0 and not game_over:
        glutSwapBuffers()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the falling diamond
        diamond(x, diamond_y, color)

        # Draw the catcher
        catcher(catcher_x, 10, catcher_color)

        # Use double buffering
        glutSwapBuffers()

        # Ensure the frame buffer is bound
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Copy the contents of the frame buffer to the texture
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, W_WIDTH, W_HEIGHT, 0)

        # Redraw the entire scene from the copied texture
        glRasterPos2i(0, W_HEIGHT)
        glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, W_WIDTH, W_HEIGHT)

        glutSwapBuffers()
        diamond_y += dy
        time.sleep(0.02)  # Adjust the sleep time for smooth animation

def draw_square(x, y, color):
    blx, bly = x, y
    brx, bry = x + 20, y
    ulx, uly = x, y + 20
    urx, ury = x + 20, y + 20
    draw_line(ulx, uly, urx, ury, color)
    draw_line(ulx, uly, blx, bly, color)
    draw_line(urx, ury, brx, bry, color)
    draw_line(blx, bly, brx, bry, color)

def fall_square(x, y, color):
    dy = -3  # Adjust the falling speed
    square_y = y

    while square_y > 0 and not game_over:
        glutSwapBuffers()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the falling square
        draw_square(x, square_y, color)

        # Draw the catcher
        catcher(catcher_x, 10, catcher_color)

        # Use double buffering
        glutSwapBuffers()

        # Ensure the frame buffer is bound
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Copy the contents of the frame buffer to the texture
        glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, W_WIDTH, W_HEIGHT, 0)

        # Redraw the entire scene from the copied texture
        glRasterPos2i(0, W_HEIGHT)
        glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 0, 0, W_WIDTH, W_HEIGHT)

        glutSwapBuffers()
        square_y += dy
        time.sleep(0.02)  # Adjust the sleep time for smooth animation

# ...

def spawn_element():

    # Generate a random number
    random_number = random.randint(0, 100)

    # Check if the number is even or odd
    if random_number % 2 == 0:
        fall_diamond(ball_x - 10, ball_y - 10, ball_color)
    else:
        fall_square(ball_x - 10, ball_y - 10, ball_color)

# ...

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


catcher_x = 350
catchbox = AABB(catcher_x, 10, 100, 20)
catcher_color = random.choice(color_set)
spawn_diamond = True
bullet_active = False
bullet_x = 0
bullet_y = 0
bullet_color = (1, 1, 1)
bullet_duration = 0.1  # in seconds
last_shoot_time = time.time()

ball_color = random.choice(color_set)
spawnx = []  # set of x values for the ball
for i in range(100):
    spawnx.append(random.randint(30, 770))

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
    global bullet_active, bullet_x, bullet_y, catcher_x

    bullet_active = True
    bullet_x = catcher_x + 50
    bullet_y = 30


def keyboard_listener(key, x, y):
    global catcher_color

    if key == b' ':
        # Change the catcher color randomly to another color
        catcher_color = random.choice([color for color in color_set if color != catcher_color])
    elif key == b'c':
        # Shoot the bullet
        if not bullet_active:
            shoot_bullet()
            last_shoot_time = time.time()


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

def mouse_click(button, state, x, y):
    global bullet_active, last_shoot_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Shoot the bullet
        if not bullet_active:
            shoot_bullet()
            last_shoot_time = time.time()

def animate():
    global ball_x, ball_y, ball_color, ballbox, game_over, spawn_diamond

    if not game_over:
        ball_y -= 1
        ballbox.y -= 1

        if ball_y <= 0:
            print("Game Over - Ball went beyond the lower boundary!")
            game_over = True
            return

        glutPostRedisplay()


def display():
    global game_over, catcher_color, ball_color, catcher_x, catcher_color, bullet_active, bullet_x, bullet_y, bullet_color, ball_x, ball_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    catcher(catcher_x, 10, catcher_color)

    update_bullet()

    if not game_over:
        if bullet_active:
            draw_line(bullet_x, bullet_y, bullet_x, bullet_y + 10, bullet_color)

            if ballbox.collides_with_bullet(bullet_x, bullet_y):
                if ball_color != catcher_color:
                    # Draw a diamond at the location where the ball disappeared
                    spawn_element()

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

        mid_circle(ball_x, ball_y, 10, ball_color)

        if ball_y < 0:
            if ball_color == catcher_color:
                catcher_color = random.choice([color for color in color_set if color != catcher_color])
            else:
                print("Game Over - Ball went beyond the lower boundary!")
                game_over = True

        if ballbox.collides_with(catchbox):
            if ball_color == catcher_color:
                catcher_color = random.choice([color for color in color_set if color != catcher_color])
                ball_color = random.choice(color_set)
                ball_x = random.choice(spawnx)
                ball_y = 630
                ballbox.x = ball_x - 10
                ballbox.y = ball_y - 10
            else:
                print("Game Over - Catcher collided with a ball of different color!")
                game_over = True

    glutSwapBuffers()
# ... (Other code remains unchanged)
def main():
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

    glOrtho(0, W_WIDTH, 0, W_HEIGHT, -1, 1)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glutMainLoop()

if __name__ == "__main__":
    main()