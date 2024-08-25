import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

azimuth = 45
elevation = 35.264

start_x = 0
start_y = 0
last_x = 0
last_y = 0

trans_u = 0
trans_v = 0
up = 1

zoom_rate = 5

at = np.array([0, 0, 0])

is_press = 0

is_ortho = 0

def drawFrame():
    glBegin(GL_LINES)

    glColor3ub(255, 0, 0)
    glVertex3fv((np.array([-5.,0.,0.,1.]))[:-1])
    glVertex3fv((np.array([5.,0.,0.,1.]))[:-1])

    glColor3ub(0, 255, 0)
    glVertex3fv((np.array([0.,0.,-5.,1.]))[:-1])
    glVertex3fv((np.array([0.,0.,5.,1.]))[:-1])

    # y-axis
    # glColor3ub(0, 0, 255)
    # glVertex3fv((np.array([0.,0.,0.,1.]))[:-1])
    # glVertex3fv((np.array([0.,5.,0.,1.]))[:-1])

    glColor3ub(255, 255, 255)
    for i in range(0, 11):
        glVertex3fv((np.array([-5., 0., i/2,1.]))[:-1])
        glVertex3fv((np.array([5., 0., i/2,1.]))[:-1])
        glVertex3fv((np.array([-5., 0., -i/2,1.]))[:-1])
        glVertex3fv((np.array([5., 0., -i/2,1.]))[:-1])

    for i in range(0, 11):
        glVertex3fv((np.array([i/2., 0., -5,1.]))[:-1])
        glVertex3fv((np.array([i/2, 0., 5,1.]))[:-1])
        glVertex3fv((np.array([-i/2., 0., -5,1.]))[:-1])
        glVertex3fv((np.array([-i/2, 0., 5,1.]))[:-1])

    glEnd()

def render():
    global elevation
    global azimuth
    global up

    if elevation > 360:
        elevation = elevation - 360
    elif elevation < 0:
        elevation = elevation + 360
    if np.radians(elevation) >= 0 and np.radians(elevation) <= np.pi/2:
        up = 1
    elif np.radians(elevation) > np.pi/2 and np.radians(elevation) <= np.pi:
        up = -1
    elif np.radians(elevation) > np.pi and np.radians(elevation) <= 3*np.pi/2:
        up = -1
    elif np.radians(elevation) > 3*np.pi/2 and np.radians(elevation) <= 2*np.pi:
        up = 1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    # Projection transformation
    if is_ortho == 0:
        gluPerspective(60, 1, 1, 100)
    elif is_ortho == 1:
        glOrtho(-zoom_rate*2, zoom_rate*2, -zoom_rate*2, zoom_rate*2, -zoom_rate*4, zoom_rate*4)

    # Viewing transformation
    myLookat()

    # Modeling transformation
    drawFrame()

def camera_vector():
    global elevation, azimuth, up

    x = np.cos(np.radians(elevation)) * np.sin(np.radians(azimuth))
    y = np.sin(np.radians(elevation))
    z = np.cos(np.radians(elevation)) *  np.cos(np.radians(azimuth))
    w = np.array([x, y, z])
    u = np.cross(np.array([0, up, 0]), w)
    u = u / np.linalg.norm(u)
    v = np.cross(w, u)
    v = v / np.linalg.norm(v)

    return w, u, v

def myLookat():
    (w, u, v) = camera_vector()
    viewing = np.array([[u[0], v[0], w[0], zoom_rate*w[0] + at[0]],
                        [u[1], v[1], w[1], zoom_rate*w[1] + at[1]],
                        [u[2], v[2], w[2], zoom_rate*w[2] + at[2]],
                        [   0,    0,    0, 1]])
    viewing = np.linalg.inv(viewing)
    glMultMatrixf(viewing.T)

def key_callback(window, key, scancode, action, mods):
    global is_ortho
    if key==glfw.KEY_V:
        if action==glfw.PRESS:
            if is_ortho == 0:
                is_ortho = 1
            elif is_ortho == 1:
                is_ortho = 0

def cursor_callback(window, xpos, ypos):
    global azimuth, elevation
    global is_press
    global start_x, start_y
    global last_x, last_y
    global trans_u, trans_v
    global at
    if is_press == 1:
        last_x = xpos
        last_y = ypos
        elevation = elevation + np.radians((last_y - start_y) * 10)
        azimuth = azimuth + np.radians((start_x - last_x) * 10)
        start_x = last_x
        start_y = last_y
        
    elif is_press == 2:
        (w, u, v) = camera_vector()
        last_x = xpos
        last_y = ypos
        trans_u = (start_x - last_x) * 0.005
        trans_v = (last_y - start_y) * 0.005
        at = at + u*trans_u + v*trans_v
        start_x = last_x
        start_y = last_y

def button_callback(window, button, action, mod):
    global start_x, start_y
    global is_press

    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            start_x = glfw.get_cursor_pos(window)[0]
            start_y = glfw.get_cursor_pos(window)[1]
            is_press = 1
        elif action==glfw.RELEASE:
            is_press = 0
        
    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            start_x = glfw.get_cursor_pos(window)[0]
            start_y = glfw.get_cursor_pos(window)[1]
            is_press = 2
        elif action==glfw.RELEASE:
            is_press = 0
     
def scroll_callback(window, xoffset, yoffset):
    global zoom_rate
    if yoffset == 1:
        if zoom_rate <= 0.1:
            zoom_rate = 0.1
        else:
            zoom_rate = zoom_rate - 0.1
    elif yoffset == -1:
        if zoom_rate >= 10:
            zoom_rate = 10
        else:
            zoom_rate = zoom_rate + 0.1

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 960, "Class_Assignment1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()