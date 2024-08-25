from shutil import move
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

is_box = 0
is_move = 0

file_name = ''
parent = 'Root'
currentJoint = 'root'
parentPosition = np.array([0, 0, 0])
currentPosition = np.array([0, 0, 0])
stack = []
motion = []
global_frame = 1
global_fps = 0
press_time = 0
motion_count = 0

gVertexArrayIndexed = None
gIndexArray = None

def createVertexAndIndexArrayIndexed():
    if 'sample' not in file_name:
        varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -.3 ,  1 ,  .3 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  .3 ,  1 ,  .3 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  .3 ,  0 ,  .3 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -.3 ,  0 ,  .3 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -.3 ,  1 , -.3 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  .3 ,  1 , -.3 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  .3 ,  0 , -.3 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -.3 ,  0 , -.3 ), # v7
            ], 'float32')
    elif 'sample' in file_name:
        varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -.02 ,  1 ,  .02 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  .02 ,  1 ,  .02 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  .02 ,  0 ,  .02 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -.02 ,  0 ,  .02 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -.02 ,  1 , -.02 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  .02 ,  1 , -.02 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  .02 ,  0 , -.02 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -.02 ,  0 , -.02 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

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
    global currentPosition

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

    if 'sample' not in file_name:
        glScalef(0.05, 0.05, 0.05)
    draw_stack()

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
    global is_ortho, is_box, is_move, press_time
    if key==glfw.KEY_V:
        if action==glfw.PRESS:
            if is_ortho == 0:
                is_ortho = 1
            elif is_ortho == 1:
                is_ortho = 0
    if key==glfw.KEY_1:
        if action==glfw.PRESS:
            is_box = 0
    if key==glfw.KEY_2:
        if action==glfw.PRESS:
            is_box = 1
    if key==glfw.KEY_SPACE:
        if action==glfw.PRESS:
            is_move = 1
            press_time = glfw.get_time()

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

def draw_stack():
    global parentPosition, currentPosition, press_time, global_fps, global_frame, motion_count
    drawing_stack = []
    is_end = 0
    frame_num = int((glfw.get_time() - press_time) * global_fps) % global_frame
    motion_count = 0
    for joint in stack:
        if joint.parent == 'Root':
            drawing_stack.append(joint)
            glPushMatrix()
            currentPosition = np.array([joint.offset[0], joint.offset[1], joint.offset[2]])
            glTranslatef(joint.offset[0], joint.offset[1], joint.offset[2])

            if is_move == 1:
                for i in range(0, int(joint.channel_num)):
                    animate(int(frame_num), motion_count, joint.channel[i])
                    motion_count += 1
        elif joint.name == 'End':
            ## final end joint
            if joint.parent == stack[-1].parent and joint.name == stack[-1].name:
                drawing_stack.append(joint)
                parentPosition = np.array([0, 0, 0])
                currentPosition = np.array([joint.offset[0], joint.offset[1], joint.offset[2]])
                if is_box == 0:
                    draw_line()
                elif is_box == 1:
                    draw_cube(joint.offset)
                glPushMatrix()
                glTranslatef(joint.offset[0], joint.offset[1], joint.offset[2])
                for i in reversed(drawing_stack):
                    del drawing_stack[-1]
                    glPopMatrix()
                continue
            drawing_stack.append(joint)
            parentPosition = np.array([0, 0, 0])
            currentPosition = np.array([joint.offset[0], joint.offset[1], joint.offset[2]])
            if is_box == 0:
                draw_line()
            elif is_box == 1:
                draw_cube(joint.offset)
            glPushMatrix()
            glTranslatef(joint.offset[0], joint.offset[1], joint.offset[2])
            is_end = 1
        else:
            ## End state's next line
            if is_end == 1:
                for i in reversed(drawing_stack):
                    if joint.parent == i.name:
                        break
                    del drawing_stack[-1]
                    glPopMatrix()
            is_end = 0
            drawing_stack.append(joint)
            parentPosition = np.array([0, 0, 0])
            currentPosition = np.array([joint.offset[0], joint.offset[1], joint.offset[2]])
            if is_box == 0:
                draw_line()
            elif is_box == 1:
                draw_cube(joint.offset)
            glPushMatrix()
            glTranslatef(joint.offset[0], joint.offset[1], joint.offset[2])

            if is_move == 1:
                for i in range(0, int(joint.channel_num)):
                    animate(int(frame_num), motion_count, joint.channel[i])
                    motion_count += 1
                    if motion_count == int(joint.channel_num) + 1:
                        motion_count = 0

def draw_line():
    glBegin(GL_LINES)
    glColor3ub(0, 0, 255)
    glVertex3fv(currentPosition)
    glVertex3fv(parentPosition)
    glEnd()

def draw_cube(offset):
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray

    offset_norm = np.linalg.norm(offset)
    direct = np.cross(offset / offset_norm, np.array([0, 1, 0]))
    degreeSize = np.rad2deg(np.arcsin(np.sqrt(direct[0]**2 + direct[1]**2 + direct[2]**2)))
    if np.dot(offset, np.array([0, 1, 0])) > 0:
        degreeSize = 180 - degreeSize

    glPushMatrix()
    glRotatef(degreeSize, direct[0], direct[1], direct[2])
    glScalef(1, -offset_norm, 1)
    glColor3ub(0, 0, 255)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
    glPopMatrix()

def animate(frame_num, motion_count, channel):
    if channel.upper() == 'XPOSITION':
        glTranslatef(np.float32(motion[frame_num][motion_count]), 0, 0)
    elif channel.upper() == 'YPOSITION':
        glTranslatef(0, np.float32(motion[frame_num][motion_count]), 0)
    elif channel.upper() == 'ZPOSITION':
        glTranslatef(0, 0, np.float32(motion[frame_num][motion_count]))
    elif channel.upper() == 'XROTATION':
        glRotatef(np.float32(motion[frame_num][motion_count]), 1, 0, 0)
    elif channel.upper() == 'YROTATION':
        glRotatef(np.float32(motion[frame_num][motion_count]), 0, 1, 0)
    elif channel.upper() == 'ZROTATION':
        glRotatef(np.float32(motion[frame_num][motion_count]), 0, 0, 1)

class Joint:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.child = []

    def set_offset(self, offset):
        self.offset = offset
    def set_channel(self, channel_num, channel):
        self.channel_num = channel_num
        self.channel = channel

def drop_callback(window, paths):
    global parent, currentJoint, currentPosition, parentPosition, is_move, is_box
    global stack, motion, global_fps, global_frame, press_time, file_name

    is_box = 0
    is_move = 0
    parent = 'Root'
    currentJoint = 'root'
    parentPosition = np.array([0, 0, 0])
    currentPosition = np.array([0, 0, 0])
    stack = []
    motion = []
    global_frame = 1
    global_fps = 0
    press_time = 0

    joints_num = 0
    joints = []
    is_motion = 0

    file_name = paths[0].split('\\')[-1]
    single_obj = open(paths[0], 'r')
    lines = single_obj.readlines()
    for line in lines:
        line = line.strip()
        if 'Frames' in line:
            frame = line[7:]
        elif 'Frame Time' in line:
            fps = 1 / float(line[12:])
        elif 'ROOT' in line:
            joints_num = joints_num + 1
            tmp = line.split(' ')
            joints.append(tmp[-1])

            currentJoint = tmp[-1]
            root = Joint('Root', currentJoint)
            stack.append(root)
        elif 'JOINT' in line:
            joints_num = joints_num + 1
            tmp = line.split(' ')
            joints.append(tmp[-1])

            parent = currentJoint
            currentJoint = tmp[-1]
            joint = Joint(parent, currentJoint)
            stack.append(joint)
        elif 'End' in line:
            parent = currentJoint
            currentJoint = 'End'
            joint = Joint(parent, currentJoint)
            joint.set_channel(0, None)
            stack.append(joint)
        elif '}' in line:
            currentJoint = parent
            for join in stack:
                if join.name == currentJoint:
                    parent = join.parent
        elif 'OFFSET' in line:
            tmp = line.split(' ')
            for join in stack:
                if join.name == currentJoint and join.parent == parent:
                    join.set_offset(np.array([float(tmp[1]), float(tmp[2]), float(tmp[3])]))
        elif 'CHANNELS' in line:
            tmp = line.split(' ')
            for join in stack:
                if join.name == currentJoint:
                    join.set_channel(tmp[1], tmp[2:])
        elif 'MOTION' in line:
            is_motion = 1
        if is_motion == 1:
            line = line.replace('\t', ' ')
            line = line.split(' ')
            motion.append(line)

    motion = motion[3:]
    frame = frame.replace('\t', '')
    global_fps = np.float32(fps)
    global_frame = np.float32(frame)
    print('File name: ' + file_name)
    print('Number of frames: ' + frame)
    print('FPS: ' + str(fps))
    print('Number of joints: ' + str(joints_num))
    print('List of all joint names: ' + str(joints))

def main():
    global gVertexArrayIndexed, gIndexArray

    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 960, "Class_Assignment3", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        glfw.swap_interval(1)
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()