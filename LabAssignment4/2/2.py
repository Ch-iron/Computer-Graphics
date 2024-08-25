import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(M): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity()
    # draw cooridnate 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd()
    glColor3ub(255, 255, 255)
    # draw point p 
    glBegin(GL_POINTS) 
    # your implementation
    glVertex2fv( (M @ np.array([.5,0.,1.])) [:-1] )
    glEnd()
    # draw vector v 
    glBegin(GL_LINES) 
    # your implementation
    glColor3ub(255, 255, 255) 
    glVertex2fv( (M @ np.array([.5,0.,0.])) [:-1] )
    glVertex2fv( (M @ np.array([0.,0.,0.])) [:-1] )
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

    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()
        
        s = np.sin(t)
        c = np.cos(t)
        R = np.array([[c, -s, 0.],
                      [s, c, 0.],
                      [0., 0., 1.]])

        T = np.array([[1., 0., .5],
                      [0., 1., 0.],
                      [0., 0., 1.]])
        render(R @ T)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()