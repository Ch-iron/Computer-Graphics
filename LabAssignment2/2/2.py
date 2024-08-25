import glfw
from OpenGL.GL import *

primitive_type = {
    '1': GL_POINTS,
    '2': GL_LINES,
    '3': GL_LINE_STRIP,
    '4': GL_LINE_LOOP,
    '5': GL_TRIANGLES,
    '6': GL_TRIANGLE_STRIP,
    '7': GL_TRIANGLE_FAN,
    '8': GL_QUADS,
    '9': GL_QUAD_STRIP,
    '10': GL_POLYGON 
}

def render(type):
    if type == '0':
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(primitive_type.get('10'))
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glEnd()
    elif type == '10':
        print('wrong input value. input 0~9')
    elif type in primitive_type:
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(primitive_type.get(type))
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glEnd()
    else:
        print('wrong input value. input 0~9')

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2015005187", None,None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # # Poll events
    glfw.poll_events()

    # Render here, e.g. using pyOpenGL
    render('4')

    # Swap front and back buffers
    glfw.swap_buffers(window)
        
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        type = input()

        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render(type)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()