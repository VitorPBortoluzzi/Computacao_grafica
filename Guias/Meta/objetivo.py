import pyglet
pyglet.options['shadow_window'] = False
pyglet.window.Window(visible=False)

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
from pywavefront import Wavefront

import math

# =====================================================
# CAMERA
# =====================================================

camera_x = 0
camera_y = 2
camera_z = -15

yaw = 0
pitch = 0

sensitivity = 0.15

# =====================================================
# TEXTURA
# =====================================================

def load_texture(filename):

    img = Image.open(filename)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = img.convert("RGBA").tobytes()

    width, height = img.size

    tex_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data
    )

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id


# =====================================================
# DIREÇÃO DA CAMERA
# =====================================================

def update_camera_direction():

    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw)
    dir_y = math.sin(rad_pitch)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw)

    return dir_x, dir_y, dir_z


# =====================================================
# CUBO
# =====================================================

cube_vertices = [

    (-1,-1,-1),
    ( 1,-1,-1),
    ( 1, 1,-1),
    (-1, 1,-1),

    (-1,-1, 1),
    ( 1,-1, 1),
    ( 1, 1, 1),
    (-1, 1, 1)
]


def draw_textured_cube():

    glBegin(GL_QUADS)

    # trás
    glNormal3f(0,0,-1)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[2])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[3])

    # frente
    glNormal3f(0,0,1)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[4])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[5])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[7])

    # baixo
    glNormal3f(0,-1,0)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[5])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[4])

    # cima
    glNormal3f(0,1,0)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[3])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[7])

    # direita
    glNormal3f(1,0,0)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[2])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[5])

    # esquerda
    glNormal3f(-1,0,0)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[3])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[7])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[4])

    glEnd()


# =====================================================
# OBJ
# =====================================================

def draw_obj_model(scene, tex_id):

    glBindTexture(GL_TEXTURE_2D, tex_id)

    for mat in scene.materials.values():

        verts = mat.vertices

        count = len(verts) // 8

        array_type = (GLfloat * len(verts))(*verts)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glInterleavedArrays(
            GL_T2F_N3F_V3F,
            0,
            array_type
        )

        glDrawArrays(GL_TRIANGLES, 0, count)

        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


# =====================================================
# OPENGL
# =====================================================

def init_opengl(display):

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glLightModelfv(
        GL_LIGHT_MODEL_AMBIENT,
        (0.3,0.3,0.3,1)
    )

    glLightfv(
        GL_LIGHT0,
        GL_DIFFUSE,
        (1,1,1,1)
    )

    glLightfv(
        GL_LIGHT0,
        GL_SPECULAR,
        (1,1,1,1)
    )

    glMaterialfv(
        GL_FRONT,
        GL_SPECULAR,
        (1,1,1,1)
    )

    glMaterialf(
        GL_FRONT,
        GL_SHININESS,
        80
    )

    glMatrixMode(GL_PROJECTION)

    gluPerspective(
        45,
        display[0]/display[1],
        0.1,
        200
    )

    glMatrixMode(GL_MODELVIEW)


# =====================================================
# MAIN
# =====================================================

def main():

    global camera_x
    global camera_y
    global camera_z
    global yaw
    global pitch

    pygame.init()

    display = (1280,720)

    pygame.display.set_mode(
        display,
        DOUBLEBUF | OPENGL
    )

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    init_opengl(display)

    # TEXTURAS

    tex_grama = load_texture("texturas/grama.jpg")
    tex_parede = load_texture("texturas/parede.jpg")
    tex_madeira = load_texture("texturas/madeira.jpg")

    # OBJS

    cat_scene = Wavefront(
        "OBJS/Cat/Cat.obj",
        collect_faces=True,
        parse=True
    )

    cat_tex = load_texture(
        "OBJS/Cat/Cat_diffuse.jpg"
    )

    tree_scene = Wavefront(
        "OBJS/Tree/Tree.obj",
        collect_faces=True,
        parse=True
    )

    tree_tex = load_texture(
        "OBJS/Tree/Tree.jpg"
    )

    car_scene = Wavefront(
        "OBJS/Car/Car.obj",
        collect_faces=True,
        parse=True
    )

    car_tex = load_texture(
        "OBJS/Car/Car.jpg"
    )

    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

        dx, dy = pygame.mouse.get_rel()

        yaw += dx * sensitivity
        pitch -= dy * sensitivity

        dir_x, dir_y, dir_z = update_camera_direction()

        keys = pygame.key.get_pressed()

        speed = 0.3

        if keys[K_w]:
            camera_x += dir_x * speed
            camera_z += dir_z * speed

        if keys[K_s]:
            camera_x -= dir_x * speed
            camera_z -= dir_z * speed

        if keys[K_a]:
            camera_x += dir_z * speed
            camera_z -= dir_x * speed

        if keys[K_d]:
            camera_x -= dir_z * speed
            camera_z += dir_x * speed

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        glLoadIdentity()

        gluLookAt(
            camera_x,
            camera_y,
            camera_z,

            camera_x + dir_x,
            camera_y + dir_y,
            camera_z + dir_z,

            0,1,0
        )

        glLightfv(
            GL_LIGHT0,
            GL_POSITION,
            (0,15,0,1)
        )

        # ========================
        # CHÃO
        # ========================

        glBindTexture(GL_TEXTURE_2D, tex_grama)

        glPushMatrix()

        glTranslatef(0,-2,0)
        glScalef(30,0.1,30)

        draw_textured_cube()

        glPopMatrix()

        # ========================
        # PAREDES
        # ========================

        glBindTexture(GL_TEXTURE_2D, tex_parede)

        paredes = [

            (0,3,30,0),
            (0,3,-30,0),
            (30,3,0,90),
            (-30,3,0,90)

        ]

        for x,y,z,r in paredes:

            glPushMatrix()

            glTranslatef(x,y,z)

            if r:
                glRotatef(r,0,1,0)

            glScalef(30,5,0.2)

            draw_textured_cube()

            glPopMatrix()

        # ========================
        # CERCA
        # ========================

        glBindTexture(GL_TEXTURE_2D, tex_madeira)

        for i in range(-20,21,4):

            glPushMatrix()

            glTranslatef(i,-0.5,10)
            glScalef(0.2,2,0.2)

            draw_textured_cube()

            glPopMatrix()

        # ========================
        # GATO
        # ========================

        glPushMatrix()

        glTranslatef(0,-1,0)

        glRotatef(-90,1,0,0)

        glScalef(
            0.02,
            0.02,
            0.02
        )

        draw_obj_model(
            cat_scene,
            cat_tex
        )

        glPopMatrix()

        # ========================
        # ÁRVORE
        # ========================

        glPushMatrix()

        glTranslatef(-8,-2,5)

        glRotatef(-90,1,0,0)

        glScalef(
            0.5,
            0.5,
            0.5
        )

        draw_obj_model(
            tree_scene,
            tree_tex
        )

        glPopMatrix()

        # ========================
        # CARRO
        # ========================

        glPushMatrix()

        glTranslatef(8,-2,-5)

        glRotatef(180,0,1,0)

        glScalef(
            0.03,
            0.03,
            0.03
        )

        draw_obj_model(
            car_scene,
            car_tex
        )

        glPopMatrix()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()