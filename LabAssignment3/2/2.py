import glfw
from OpenGL.GL import *
import numpy as np

tendegree = np.pi / 18

transformation = {
    'W': np.array([[0.9, 0., 0.],
                   [0., 0.9, 0.],
                   [0., 0., 1.]]),
    'E': np.array([[1.1, 0., 0.],
                   [0., 1.1, 0.],
                   [0., 0., 1.]]),
    'S': np.array([[np.cos(tendegree), -np.sin(tendegree), 0.],
                   [np.sin(tendegree), np.cos(tendegree), 0.],
                   [0., 0., 1.]]),
    'D': np.array([[np.cos(tendegree), np.sin(tendegree), 0.],
                   [-np.sin(tendegree), np.cos(tendegree), 0.],
                   [0., 0., 1.]]),
    'X': np.array([[1., -0.1, 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]]),
    'C': np.array([[1., 0.1, 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]]),
    'R': np.array([[1., 0., 0.],
                   [0., -1., 0.],
                   [0., 0., 1.]]),
    '1': np.array([[1., 0., 0.],
                   [0., 1., 0.],
                   [0., 0., 1.]]),
}

gComposedM = np.array([[1., 0., 0.],
                       [0., 1., 0.],
                       [0., 0., 1.]])
def compose(type):
    global gComposedM

    if type == '1':
        gComposedM = transformation.get(type)
    else:
        newM = transformation.get(type)
        gComposedM = newM @ gComposedM

def render(T):
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
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.])) [:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.])) [:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.])) [:-1] )
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2015005187", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.poll_events()

    render(gComposedM)

    glfw.swap_buffers(window)

    while not glfw.window_should_close(window):
        trans = input()
        compose(trans)

        glfw.poll_events()

        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()