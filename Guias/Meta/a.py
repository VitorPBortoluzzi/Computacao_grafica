
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import math

# =====================================================
# CAMERA
# =====================================================

camera_x = 0
camera_y = 2
camera_z = -20

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
# CAMERA DIRECTION
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

    # traseira
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
# OPENGL
# =====================================================

def init_opengl(display):

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE
    )

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

    glMatrixMode(GL_PROJECTION)

    gluPerspective(
        45,
        display[0]/display[1],
        0.1,
        300
    )

    glMatrixMode(GL_MODELVIEW)

# =====================================================
# CENÁRIO
# =====================================================

def draw_ground(tex):

    glBindTexture(GL_TEXTURE_2D, tex)

    glPushMatrix()
    glTranslatef(0,-2,0)
    glScalef(40,0.1,40)
    draw_textured_cube()
    glPopMatrix()

def draw_walls(tex):

    glBindTexture(GL_TEXTURE_2D, tex)

    paredes = [
        (0,3,40,0),
        (0,3,-40,0),
        (40,3,0,90),
        (-40,3,0,90)
    ]

    for x,y,z,r in paredes:

        glPushMatrix()

        glTranslatef(x,y,z)
        glRotatef(r,0,1,0)

        glScalef(40,5,0.2)

        draw_textured_cube()

        glPopMatrix()

def draw_house(tex_wall, tex_wood):

    glBindTexture(GL_TEXTURE_2D, tex_wall)

    partes = [
        (0,1,15,0,5,3,0.2),
        (0,1,5,0,5,3,0.2),
        (-5,1,10,90,5,3,0.2),
        (5,1,10,90,5,3,0.2)
    ]

    for x,y,z,r,sx,sy,sz in partes:

        glPushMatrix()

        glTranslatef(x,y,z)
        glRotatef(r,0,1,0)
        glScalef(sx,sy,sz)

        draw_textured_cube()

        glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, tex_wood)

    # telhado

    glPushMatrix()
    glTranslatef(0,4.5,10)
    glScalef(6,0.3,6)
    draw_textured_cube()
    glPopMatrix()

    # porta

    glPushMatrix()
    glTranslatef(0,-0.5,15.3)
    glScalef(0.8,1.5,0.1)
    draw_textured_cube()
    glPopMatrix()

def draw_fence(tex):

    glBindTexture(GL_TEXTURE_2D, tex)

    for i in range(-15,16,3):

        glPushMatrix()

        glTranslatef(i,-0.5,25)
        glScalef(0.2,2,0.2)

        draw_textured_cube()

        glPopMatrix()

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

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    init_opengl(display)

    tex_grama = load_texture("texturas/grama.jpg")
    tex_parede = load_texture("texturas/parede.jpg")
    tex_madeira = load_texture("texturas/madeira.jpg")

    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        dx, dy = pygame.mouse.get_rel()

        yaw += dx * sensitivity
        pitch -= dy * sensitivity

        pitch = max(-89, min(89, pitch))

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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        gluLookAt(
            camera_x, camera_y, camera_z,
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

        draw_ground(tex_grama)
        draw_walls(tex_parede)
        draw_house(tex_parede, tex_madeira)
        draw_fence(tex_madeira)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

