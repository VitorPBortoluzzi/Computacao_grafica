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
sensitivity = 0.02
rot_x, rot_y = 0,0


def update_camera_direction():
    rad_yaw = math.radians(yaw) # Converte graus do Yaw para radianos (exigência do math.sin/cos)
    rad_pitch = math.radians(pitch) # Converte graus do Pitch para radianos
    
    # Cálculo das componentes do vetor de direção usando trigonometria esférica
    dir_x = math.cos(rad_pitch) * math.sin(rad_yaw) # Componente X da direção
    dir_y = math.sin(rad_pitch)                      # Componente Y da direção (altura do olhar)
    dir_z = math.cos(rad_pitch) * math.cos(rad_yaw) # Componente Z da direção (profundidade)
    return dir_x, dir_y, dir_z # Retorna o vetor unitário de direção

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