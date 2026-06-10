import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import math

from pywavefront import Wavefront

import pyglet

pyglet.options['shadow_window'] = False
pyglet.window.Window(visible=False)

# ==================================================
# CAMERA
# ==================================================

camera_x = 0
camera_y = 1.5
camera_z = 0

yaw = 0
pitch = 0

sensitivity = 0.2

# ==================================================
# TEXTURAS
# ==================================================

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


# ==================================================
# DIREÇÃO DA CAMERA
# ==================================================

def update_camera_direction():

    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw)
    dir_y = math.sin(rad_pitch)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw)

    return dir_x, dir_y, dir_z


# ==================================================
# CUBO
# ==================================================

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

    # frontal
    glNormal3f(0,0,1)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[4])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[5])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[6])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[7])

    # inferior
    glNormal3f(0,-1,0)

    glTexCoord2f(0,0); glVertex3fv(cube_vertices[0])
    glTexCoord2f(1,0); glVertex3fv(cube_vertices[1])
    glTexCoord2f(1,1); glVertex3fv(cube_vertices[5])
    glTexCoord2f(0,1); glVertex3fv(cube_vertices[4])

    # superior
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


# ==================================================
# OPENGL
# ==================================================

def init_opengl(display):

    glEnable(GL_DEPTH_TEST)

    glEnable(GL_TEXTURE_2D)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE
    )

    # glLightfv(
    #     GL_LIGHT0,
    #     GL_POSITION,
    #     (0, 30, -5, 1)
    # )

    # Luz ambiente

    glLightModelfv(
        GL_LIGHT_MODEL_AMBIENT,
        (0.6, 0.6, 0.9, 1.0)
    )

    # Luz difusa

    glLightfv(
        GL_LIGHT0,
        GL_DIFFUSE,
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
        display[0] / display[1],
        0.1,
        200
    )

    glMatrixMode(GL_MODELVIEW)


#==================
#=======Chão=======
#==================

def draw_chao(tex_grama):

    glBindTexture(GL_TEXTURE_2D, tex_grama)

    glPushMatrix()

    glTranslatef(0,-2,0)

    glScalef(40,0.1,40)

    draw_textured_cube()

    glPopMatrix()

    

def draw_paredes(tex_parede):

    glBindTexture(GL_TEXTURE_2D, tex_parede)

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

def draw_casa(tex_parede,tex_madeira):
    
    # frente 
    glBindTexture(GL_TEXTURE_2D, tex_parede)

    glPushMatrix()

    glTranslatef(0,1,25)

    glScalef(5,3,0.2)

    draw_textured_cube()

    glPopMatrix()

    #tras

    glPushMatrix()

    glTranslatef(0,1,15)

    glScalef(5,3,0.2)

    draw_textured_cube()

    glPopMatrix()

    #esquerda
    glPushMatrix()

    glTranslatef(-5,1,20)

    glRotatef(90,0,1,0)

    glScalef(5,3,0.2)

    draw_textured_cube()

    glPopMatrix()

    #direita
    glPushMatrix()

    glTranslatef(5,1,20)

    glRotatef(90,0,1,0)

    glScalef(5,3,0.2)

    draw_textured_cube()

    glPopMatrix()

    #telhado
    glBindTexture(GL_TEXTURE_2D, tex_madeira)

    glPushMatrix()

    glTranslatef(0,4.5,20)

    glScalef(6,0.3,6)

    draw_textured_cube()

    glPopMatrix()

#porta
    glPushMatrix()

    glTranslatef(0,-0.5,14.7)

    glScalef(0.8,1.5,0.1)

    draw_textured_cube()

    glPopMatrix()

    #janelas
    glPushMatrix()

    glTranslatef(-2,1,14.7)

    glScalef(0.5,0.5,0.1)

    draw_textured_cube()

    glPopMatrix()

    glPushMatrix()

    glTranslatef( 2,1,14.7)

    glScalef(0.5,0.5,0.1)

    draw_textured_cube()

    glPopMatrix()

def draw_cerca(tex_madeira):
    glBindTexture(GL_TEXTURE_2D, tex_madeira)

    for i in range(-40,40,3):

        glPushMatrix()

        glTranslatef(i,-0.5,0)

        glScalef(0.2,2,0.2)

        draw_textured_cube()

        glPopMatrix()


    glPushMatrix()

    glTranslatef(0, 0.3, 0)

    glScalef(40, 0.1, 0.1)

    draw_textured_cube()

    glPopMatrix()


    glPushMatrix()

    glTranslatef(0, 1.0, 0)

    glScalef(40, 0.1, 0.1)

    draw_textured_cube()

    glPopMatrix()

def draw_obj_model(scene, tex_id):
    glEnable(GL_TEXTURE_2D) # Garante que texturas estão ligadas
    glBindTexture(GL_TEXTURE_2D, tex_id) # Vincula a textura do modelo
    for mat in scene.materials.values(): # Percorre os materiais do objeto OBJ
        verts = mat.vertices  # Pega a lista de dados [x,y,z, nx,ny,nz, u,v]
        count = len(verts) // 8 # Cada vértice tem 8 valores
        array_type = (GLfloat * len(verts))(*verts) # Converte para o formato de array do C (usado pelo OpenGL)
        glEnableClientState(GL_VERTEX_ARRAY) # Habilita o uso de arrays de vértices na GPU
        glEnableClientState(GL_NORMAL_ARRAY) # Habilita o uso de vetores normais (para luz)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY) # Habilita o uso de coordenadas de textura
        # T2F_N3F_V3F indica que o array contém: Texture (2 floats), Normal (3 floats), Vertex (3 floats)
        glInterleavedArrays(GL_T2F_N3F_V3F, 0, array_type) 
        glDrawArrays(GL_TRIANGLES, 0, count) # Desenha todos os triângulos do modelo de uma vez
        glDisableClientState(GL_TEXTURE_COORD_ARRAY) # Desabilita os estados para não afetar outros desenhos
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


def draw_cat(cat, cat_tex):

    glPushMatrix()

    # posição na fazenda
    glTranslatef(0, -1, 10)

    # orientação
    glRotatef(180, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)

    # tamanho
    glScalef(0.02, 0.02, 0.02)

    draw_obj_model(cat, cat_tex)

    glPopMatrix()

# ==================================================
# MAIN
# ==================================================

def main():

    global camera_x
    global camera_y
    global camera_z
    global yaw
    global pitch

    pygame.init()

    display = (1280, 720)

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

    cat_tex = load_texture("OBJS/Cat/Cat_diffuse.jpg")

    cat = Wavefront(
        "OBJS/Cat/Cat.obj",
        collect_faces=True,
        parse=True
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

        # Mouse

        dx, dy = pygame.mouse.get_rel()

        yaw += dx * sensitivity
        pitch -= dy * sensitivity

        pitch = max(-89, min(89, pitch))

        dir_x, dir_y, dir_z = update_camera_direction()

        # Movimento

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

            0,
            1,
            0
        )

        # Luz principal

        glLightfv(
            GL_LIGHT0,
            GL_POSITION,
            (0, 15, -5, 1)
        )

        # ==================================
        # CHÃO
        # ==================================

        draw_chao(tex_grama)

        # ==================================
        # PAREDES
        # ==================================

        draw_paredes(tex_parede)

        draw_casa(tex_parede,tex_madeira)
        # ==================================
        # CERCA
        # ==================================

        draw_cerca(tex_madeira)


        draw_cat(cat,cat_tex)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()