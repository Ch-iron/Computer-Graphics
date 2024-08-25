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
is_hierarchical_mode = 0
is_solid = 0
is_smooth = 0

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
    if is_solid == 1:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    elif is_solid == 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
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
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)
    glPushMatrix()
    lightPos0 = (6, 7, -8, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glPopMatrix()
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    glPushMatrix()
    lightPos1 = (8, 7, -6, 1)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    glPushMatrix()
    lightPos2 = (8, 8, -8, 0)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)
    glPopMatrix()
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)

    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if is_hierarchical_mode == 0:
        objectColor = (1.,0.,0.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

        glPushMatrix()
        drawObj_glDrawElements()
        glPopMatrix()
        glDisable(GL_LIGHTING)

    elif is_hierarchical_mode == 1:
        t = glfw.get_time()

        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 2 * np.sin(t), -np.sin(t))
        objectColor = (0.,0.,0.7,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/blue_whale.obj')

        glPushMatrix()
        glRotatef(210, 1, 0, 0)
        glTranslatef(0, -2, 2)
        objectColor = (0.,0.2,0.4,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/dolphin.obj')

        glPushMatrix()
        glRotatef(150, 1, 0, 0)
        glTranslatef(0, -.5, 0)
        glRotatef(t*(180/np.pi), 0, 0, 1)
        objectColor = (0.2,0.4,0.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/sea_turtle.obj')
        glPopMatrix()

        glPushMatrix()
        glRotatef(150, 1, 0, 0)
        glRotatef(t*(180/np.pi), 0, 0, 1)
        glTranslatef(1.5, 0, .5)
        objectColor = (1.,0.5,0.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/fish.obj')
        glPopMatrix()
        glPopMatrix()

        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glRotatef(90, 0, 1, 0)
        objectColor = (1.,0.8,0.6,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/aya.obj')

        glPushMatrix()
        glTranslatef(0, 1, 0)
        glRotatef(-90, 1, 0, 0)
        glRotatef(t*(180/np.pi), 0, 0, 1)
        glTranslatef(.5, 0, 0)
        objectColor = (0.6,0.3,0.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/bird.obj')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(.08, .9, .13)
        glTranslatef(0, 0.1 * np.sin(t), 0)
        objectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        drawObj_hierarchy('./obj/coffee_cup.obj')
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()

        glDisable(GL_LIGHTING)

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
    global is_ortho, is_hierarchical_mode, is_solid, is_smooth
    if key==glfw.KEY_V:
        if action==glfw.PRESS:
            if is_ortho == 0:
                is_ortho = 1
            elif is_ortho == 1:
                is_ortho = 0
    if key==glfw.KEY_H:
        if action==glfw.PRESS:
            is_hierarchical_mode = 1
    if key==glfw.KEY_Z:
        if action==glfw.PRESS:
            if is_solid == 0:
                is_solid = 1
            elif is_solid == 1:
                is_solid = 0
    if key==glfw.KEY_S:
        if action==glfw.PRESS:
            if is_smooth == 0:
                is_smooth = 1
            elif is_smooth == 1:
                is_smooth = 0

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

gVertexArrayIndexed = np.array([])
gIndexArray = np.array([])
gFlshadingVertexArray = np.array([])
gNormalArray = np.array([])
gSmshadingNormalArray = np.array([])

def drop_callback(window, paths):
    global gVertexArrayIndexed, gIndexArray, gNormalArray, gSmshadingNormalArray, gFlshadingVertexArray
    global is_hierarchical_mode

    is_hierarchical_mode = 0

    file_name = ''
    num_face = 0
    num_face3 = 0
    num_face4 = 0
    num_face_more = 0

    gVertexArrayIndexed = []
    gIndexArray = []
    gFlshadingVertexArray = []
    gNormalArray = []
    gSmshadingNormalArray = []

    file_name = paths[0].split('\\')[-1]
    single_obj = open(paths[0], 'r')
    lines = single_obj.readlines()
    for line in lines:
        line = line.strip()
        # make vertex array
        if line[0] == 'v' and line[1] != 'n':
            vertex = line.split(' ')[1:]
            gVertexArrayIndexed.append(tuple(vertex))
        elif line[0] == 'v' and line[1] == 'n':
            normal = line.split(' ')[1:]
            gNormalArray.append(tuple(normal))
        # make index array
        elif line[0] == 'f':
            num_face = num_face + 1
            indexes = line.split(' ')[1:]
            index = []
            if len(indexes) == 3:
                num_face3 = num_face3 + 1
                for i in indexes:
                    i = i.split('//')
                    index.append(i[0])
                    # make flat shading normal vector, vertex array
                    gFlshadingVertexArray.append(gNormalArray[int(i[1]) - 1])
                    gFlshadingVertexArray.append(gVertexArrayIndexed[int(i[0]) - 1])
                gIndexArray.append(tuple(index))
            elif len(indexes) >= 4:
                # triangulation
                for i in range(1, len(indexes) - 1):
                    tmp = [indexes[0], indexes[i], indexes[i + 1]]
                    for i in tmp:
                        i = i.split('//')
                        index.append(i[0])
                        gFlshadingVertexArray.append(gNormalArray[int(i[1]) - 1])
                        gFlshadingVertexArray.append(gVertexArrayIndexed[int(i[0]) - 1])
                    gIndexArray.append(tuple(index))
                    index = []
                if len(indexes) == 4:
                    num_face4 = num_face4 + 1
                else:
                    num_face_more = num_face_more + 1
    gFlshadingVertexArray = np.array(gFlshadingVertexArray, dtype=np.float32)
    gVertexArrayIndexed = np.array(gVertexArrayIndexed, dtype=np.float32)
    gIndexArray = np.array(gIndexArray, dtype=np.int32)
    # because index starts 1
    gIndexArray = gIndexArray - 1

    # get smooth shading normal vector
    for vertex in gVertexArrayIndexed:
        normals = []
        normal = [0, 0, 0]
        for i, value in enumerate(gFlshadingVertexArray):
            equal = vertex == value
            if False not in equal:
                normals.append(gFlshadingVertexArray[i - 1])
                normal = normal + gFlshadingVertexArray[i - 1]
        normal = normal / np.linalg.norm(normal)
        gSmshadingNormalArray.append(normal)
    gSmshadingNormalArray = np.array(gSmshadingNormalArray, dtype=np.float32)

    print('File name: ' + file_name)
    print('Total number of faces: ' + str(num_face))
    print('Number of faces with 3 vertices: ' + str(num_face3))
    print('Number of faces with 4 vertices: ' + str(num_face4))
    print('Number of faces with more than 4 vertices: ' + str(num_face_more))

def drawObj_glDrawElements():
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    if is_smooth == 0:
        glNormalPointer(GL_FLOAT, 6*gFlshadingVertexArray.itemsize, gFlshadingVertexArray)
        glVertexPointer(3, GL_FLOAT, 6*gFlshadingVertexArray.itemsize, ctypes.c_void_p(gFlshadingVertexArray.ctypes.data + 3*gFlshadingVertexArray.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(gFlshadingVertexArray.size/6))
    elif is_smooth == 1:
        glNormalPointer(GL_FLOAT, 3*gSmshadingNormalArray.itemsize, gSmshadingNormalArray)
        glVertexPointer(3, GL_FLOAT, 3 * gVertexArrayIndexed.itemsize, gVertexArrayIndexed)
        glDrawElements(GL_TRIANGLES, gIndexArray.size, GL_UNSIGNED_INT, gIndexArray)

wVertexArrayIndexed = np.array([])
wIndexArray = np.array([])
wFlshadingVertexArray = np.array([])
wNormalArray = np.array([])
wSmshadingNormalArray = np.array([])

dVertexArrayIndexed = np.array([])
dIndexArray = np.array([])
dFlshadingVertexArray = np.array([])
dNormalArray = np.array([])
dSmshadingNormalArray = np.array([])

hVertexArrayIndexed = np.array([])
hIndexArray = np.array([])
hFlshadingVertexArray = np.array([])
hNormalArray = np.array([])
hSmshadingNormalArray = np.array([])

sVertexArrayIndexed = np.array([])
sIndexArray = np.array([])
sFlshadingVertexArray = np.array([])
sNormalArray = np.array([])
sSmshadingNormalArray = np.array([])

fVertexArrayIndexed = np.array([])
fIndexArray = np.array([])
fFlshadingVertexArray = np.array([])
fNormalArray = np.array([])
fSmshadingNormalArray = np.array([])

bVertexArrayIndexed = np.array([])
bIndexArray = np.array([])
bFlshadingVertexArray = np.array([])
bNormalArray = np.array([])
bSmshadingNormalArray = np.array([])

cVertexArrayIndexed = np.array([])
cIndexArray = np.array([])
cFlshadingVertexArray = np.array([])
cNormalArray = np.array([])
cSmshadingNormalArray = np.array([])

def drawObj_hierarchy(path):
    global gVertexArrayIndexed, gIndexArray, gNormalArray, gSmshadingNormalArray, gFlshadingVertexArray
    global wVertexArrayIndexed, wIndexArray, wSmshadingNormalArray, wFlshadingVertexArray
    global dVertexArrayIndexed, dIndexArray, dSmshadingNormalArray, dFlshadingVertexArray
    global hVertexArrayIndexed, hIndexArray, hSmshadingNormalArray, hFlshadingVertexArray
    global sVertexArrayIndexed, sIndexArray, sSmshadingNormalArray, sFlshadingVertexArray
    global fVertexArrayIndexed, fIndexArray, fSmshadingNormalArray, fFlshadingVertexArray
    global bVertexArrayIndexed, bIndexArray, bSmshadingNormalArray, bFlshadingVertexArray
    global cVertexArrayIndexed, cIndexArray, cSmshadingNormalArray, cFlshadingVertexArray


    gVertexArrayIndexed = []
    gIndexArray = []
    gFlshadingVertexArray = []
    gNormalArray = []
    gSmshadingNormalArray = []

    file_name = path.split('/')[-1]
    single_obj = open(path, 'r')
    lines = single_obj.readlines()
    for line in lines:
        line = line.strip()
        # make vertex array
        if line == '':
            continue
        elif line[0] == 'v':
            if line[1] == 'n':
                normal = line.split(' ')[1:]
                gNormalArray.append(tuple(normal))
            elif line[1] != 't':
                vertex = line.split(' ')[1:]
                if vertex[0] == '':
                    vertex = vertex[1:]
                if file_name.split('.')[0] == 'blue_whale':
                    vertex = np.array(vertex, dtype=np.float32) / 800
                elif file_name.split('.')[0] == 'dolphin':
                    vertex = np.array(vertex, dtype=np.float32) / -150
                elif file_name.split('.')[0] == 'aya':
                    vertex = np.array(vertex, dtype=np.float32) / 1000
                elif file_name.split('.')[0] == 'sea_turtle':
                    vertex = np.array(vertex, dtype=np.float32) / 100
                elif file_name.split('.')[0] == 'fish':
                    vertex = np.array(vertex, dtype=np.float32) / 50
                elif file_name.split('.')[0] == 'bird':
                    vertex = np.array(vertex, dtype=np.float32) / 30
                elif file_name.split('.')[0] == 'coffee_cup':
                    vertex = np.array(vertex, dtype=np.float32) / 5
                gVertexArrayIndexed.append(tuple(vertex))
        elif line[0] == 'f':
            indexes = line.split(' ')[1:]
            index = []
            if len(indexes) == 3:
                for i in indexes:
                    i = i.split('/')
                    index.append(i[0])
                    # make flat shading normal vector, vertex array
                    gFlshadingVertexArray.append(gNormalArray[int(i[2]) - 1])
                    gFlshadingVertexArray.append(gVertexArrayIndexed[int(i[0]) - 1])
                gIndexArray.append(tuple(index))
            elif len(indexes) >= 4:
                # triangulation
                for i in range(1, len(indexes) - 1):
                    tmp = [indexes[0], indexes[i], indexes[i + 1]]
                    for i in tmp:
                        i = i.split('/')
                        index.append(i[0])
                        # print(i)
                        gFlshadingVertexArray.append(gNormalArray[int(i[2]) - 1])
                        gFlshadingVertexArray.append(gVertexArrayIndexed[int(i[0]) - 1])
                    gIndexArray.append(tuple(index))
                    index = []
    gFlshadingVertexArray = np.array(gFlshadingVertexArray, dtype=np.float32)
    gVertexArrayIndexed = np.array(gVertexArrayIndexed, dtype=np.float32)
    gIndexArray = np.array(gIndexArray, dtype=np.int32)
    # because index starts 1
    gIndexArray = gIndexArray - 1

    if is_smooth == 1:
        # get smooth shading normal vector
        for vertex in gVertexArrayIndexed:
            normals = []
            normal = [0, 0, 0]
            for i, value in enumerate(gFlshadingVertexArray):
                equal = vertex == value
                if False not in equal:
                    normals.append(gFlshadingVertexArray[i - 1])
                    normal = normal + gFlshadingVertexArray[i - 1]
            normal = normal / np.linalg.norm(normal)
            gSmshadingNormalArray.append(normal)
        gSmshadingNormalArray = np.array(gSmshadingNormalArray, dtype=np.float32)

    if file_name.split('.')[0] == 'blue_whale':
        wVertexArrayIndexed = gVertexArrayIndexed
        wIndexArray = gIndexArray
        wFlshadingVertexArray = gFlshadingVertexArray
        wSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = wVertexArrayIndexed
        IndexArray = wIndexArray
        FlshadingVertexArray = wFlshadingVertexArray
        SmshadingNormalArray = wSmshadingNormalArray
    elif file_name.split('.')[0] == 'dolphin':
        dVertexArrayIndexed = gVertexArrayIndexed
        dIndexArray = gIndexArray
        dFlshadingVertexArray = gFlshadingVertexArray
        dSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = dVertexArrayIndexed
        IndexArray = dIndexArray
        FlshadingVertexArray = dFlshadingVertexArray
        SmshadingNormalArray = dSmshadingNormalArray
    elif file_name.split('.')[0] == 'aya':
        hVertexArrayIndexed = gVertexArrayIndexed
        hIndexArray = gIndexArray
        hFlshadingVertexArray = gFlshadingVertexArray
        hSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = hVertexArrayIndexed
        IndexArray = hIndexArray
        FlshadingVertexArray = hFlshadingVertexArray
        SmshadingNormalArray = hSmshadingNormalArray
    elif file_name.split('.')[0] == 'sea_turtle':
        sVertexArrayIndexed = gVertexArrayIndexed
        sIndexArray = gIndexArray
        sFlshadingVertexArray = gFlshadingVertexArray
        sSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = sVertexArrayIndexed
        IndexArray = sIndexArray
        FlshadingVertexArray = sFlshadingVertexArray
        SmshadingNormalArray = sSmshadingNormalArray
    elif file_name.split('.')[0] == 'fish':
        fVertexArrayIndexed = gVertexArrayIndexed
        fIndexArray = gIndexArray
        fFlshadingVertexArray = gFlshadingVertexArray
        fSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = fVertexArrayIndexed
        IndexArray = fIndexArray
        FlshadingVertexArray = fFlshadingVertexArray
        SmshadingNormalArray = fSmshadingNormalArray
    elif file_name.split('.')[0] == 'bird':
        bVertexArrayIndexed = gVertexArrayIndexed
        bIndexArray = gIndexArray
        bFlshadingVertexArray = gFlshadingVertexArray
        bSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = bVertexArrayIndexed
        IndexArray = bIndexArray
        FlshadingVertexArray = bFlshadingVertexArray
        SmshadingNormalArray = bSmshadingNormalArray
    elif file_name.split('.')[0] == 'coffee_cup':
        cVertexArrayIndexed = gVertexArrayIndexed
        cIndexArray = gIndexArray
        cFlshadingVertexArray = gFlshadingVertexArray
        cSmshadingNormalArray = gSmshadingNormalArray

        VertexArrayIndexed = cVertexArrayIndexed
        IndexArray = cIndexArray
        FlshadingVertexArray = cFlshadingVertexArray
        SmshadingNormalArray = cSmshadingNormalArray
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    if is_smooth == 0:
        glNormalPointer(GL_FLOAT, 6*FlshadingVertexArray.itemsize, FlshadingVertexArray)
        glVertexPointer(3, GL_FLOAT, 6*FlshadingVertexArray.itemsize, ctypes.c_void_p(FlshadingVertexArray.ctypes.data + 3*FlshadingVertexArray.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(FlshadingVertexArray.size/6))
    elif is_smooth == 1:
        glNormalPointer(GL_FLOAT, 3*SmshadingNormalArray.itemsize, SmshadingNormalArray)
        glVertexPointer(3, GL_FLOAT, 3 * VertexArrayIndexed.itemsize, VertexArrayIndexed)
        glDrawElements(GL_TRIANGLES, IndexArray.size, GL_UNSIGNED_INT, IndexArray)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 960, "Class_Assignment2", None, None)
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
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()