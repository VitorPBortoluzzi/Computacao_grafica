import pygame                                # Responsável por criar a janela e capturar entrada do teclado
from pygame.locals import *                  # Importa constantes úteis do pygame (como teclas)
from OpenGL.GL import *                      # Comandos do OpenGL para renderização (ex: glBegin, glVertex, glEnable)
from OpenGL.GLU import *                     # Comandos utilitários do OpenGL (ex: gluPerspective, gluLookAt)
from PIL import Image                        # Usada para abrir e processar imagens para texturas

# Importação das bibliotecas necessárias

import pyglet
pyglet.options['shadow_window'] = False
pyglet.window.Window(visible=False)


from PIL import Image
import math


from pywavefront import Wavefront

camera_x, camera_y, camera_z = 0, 0, 0
yaw = 0
pitch = 0
sensitivity = 0.15
rot_x, rot_y = 0,0

# Função que carrega imagem como textura
def load_texture(filename):
    img = Image.open(filename) # Abre o arquivo de imagem (ex: .jpg, .png)
    img = img.transpose(Image.FLIP_TOP_BOTTOM) # Inverte a imagem (OpenGL lê de baixo para cima)
    img_data = img.convert("RGBA").tobytes() # Converte a imagem em dados binários RGBA
    width, height = img.size # Pega as dimensões da imagem em pixels
    tex_id = glGenTextures(1) # Gera um ID único para esta textura no OpenGL
    glBindTexture(GL_TEXTURE_2D, tex_id) # Ativa essa textura para configuração
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data) # Envia os dados para a GPU
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Faz a textura repetir se as coordenadas forem > 1 no eixo S (X)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # Faz a textura repetir no eixo T (Y)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # Suaviza a textura quando vista de perto
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Suaviza a textura quando vista de longe
    return tex_id # Retorna o ID para usarmos no desenho

def update_camera_direction():
    rad_yaw = math.radians(yaw) # Converte graus do Yaw para radianos (exigência do math.sin/cos)
    rad_pitch = math.radians(pitch) # Converte graus do Pitch para radianos
    
    # Cálculo das componentes do vetor de direção usando trigonometria esférica
    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw) # Componente X da direção
    dir_y = math.sin(rad_pitch)                      # Componente Y da direção (altura do olhar)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw) # Componente Z da direção (profundidade)

    return dir_x, dir_y, dir_z # Retorna o vetor unitário de direção


cube_vertices = [
    (-1, -1, -1),                            # 0 - canto inferior esquerdo traseiro
    ( 1, -1, -1),                            # 1 - canto inferior direito traseiro
    ( 1,  1, -1),                            # 2 - canto superior direito traseiro
    (-1,  1, -1),                            # 3 - canto superior esquerdo traseiro
    (-1, -1,  1),                            # 4 - canto inferior esquerdo frontal
    ( 1, -1,  1),                            # 5 - canto inferior direito frontal
    ( 1,  1,  1),                            # 6 - canto superior direito frontal
    (-1,  1,  1)                             # 7 - canto superior esquerdo frontal
]

# Índices que definem as 6 faces do cubo com 4 vértices cada
cube_faces = [
    (0, 1, 2, 3),  # Traseira
    (4, 5, 6, 7),  # Frontal
    (0, 1, 5, 4),  # Inferior
    (2, 3, 7, 6),  # Superior
    (1, 2, 6, 5),  # Lateral direita
    (0, 3, 7, 4)   # Lateral esquerda
]

# Coordenadas 2D da textura (mapeamento)
'''cube_texcoords = [
    (0, 0), # canto inferior esquerdo,
    (1, 0), # inferior direito,
    (1, 1), # superior direito,
    (0, 1)  # superior esquerdo
]'''

def draw_textured_cube():
    glBegin(GL_QUADS)  # Inicia desenho de quadriláteros

    #Explicação:
    # glTexCoord2f(0, 0)
    #→ Indica a coordenada da textura (posição do pixel da imagem que será aplicada no vértice).
    #→ Neste caso, 0,0 representa o canto inferior esquerdo da imagem.
    #--------------------------------
    #glVertex3fv(cube_vertices[0])
    #→ Indica a posição do vértice no espaço 3D onde essa parte da textura será aplicada.

    # FACE TRASEIRA (fundo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3])  # superior esquerdo

    # FACE FRONTAL (frente do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4])  # inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5])  # inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # superior esquerdo

    # FACE INFERIOR (base)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # frontal esquerda

    # FACE SUPERIOR (tampa)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3])  # traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7])  # frontal esquerda

    # FACE DIREITA (lado direito do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5])  # inferior frontal

    # FACE ESQUERDA (lado esquerdo do cubo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0])  # inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3])  # superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7])  # superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4])  # inferior frontal

    glEnd()  # Finaliza o desenho

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