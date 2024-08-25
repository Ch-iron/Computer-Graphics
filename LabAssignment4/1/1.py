import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

keys = []

def render():
    global keys
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)

    ###########################
    # implement here
    ###########################
    for key in reversed(keys):
        if key == 'Q':
            glTranslatef(-.1, 0., 0.)
        elif key == 'E':
            glTranslatef(.1, 0., 0.)
        elif key == 'A':
            glRotatef(10, 0, 0, 1)
        elif key == 'D':
            glRotatef(-10, 0, 0, 1)
        elif key =='1':
            glLoadIdentity()

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def main():
    global keys
    if not glfw.init():
        return
    window = glfw.create_window(480,480, '2015005187', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.poll_events()
    render()
    glfw.swap_buffers(window)

    while not glfw.window_should_close(window):
        key = input()
        if key == '1':
            keys = []
        else:
            keys.append(key)

        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()