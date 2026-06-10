# ==========================================================
# Ex7_Carregando_Objetos.py
# ==========================================================
#
# OpenGL Moderno
#
# Exemplo completo utilizando:
#
# - GLFW
# - VAO
# - VBO
# - Shader
# - OBJ
# - Textura
# - Câmera FPS
#
# Objetos:
#
# - Chibi
# - Gato
#
# ==========================================================


# ==========================================================
# IMPORTAÇÕES
# ==========================================================

# GLFW
#
# cria janela
# teclado
# mouse

import glfw


# OpenGL
#
# funções OpenGL

from OpenGL.GL import *

import OpenGL.GL.shaders


# numpy
#
# arrays numéricos

import numpy as np


# pyrr
#
# matrizes e vetores

import pyrr

from pyrr import Vector3


# ctypes
#
# ponteiros OpenGL

import ctypes


# ==========================================================
# ARQUIVOS AUXILIARES
# ==========================================================

# carrega textura PNG/JPG
from TextureLoader import load_texture

# câmera FPS
from Camera import Camera

# loader OBJ
from ObjLoaderSimple import ObjLoaderSimple


# ==========================================================
# OBJETO CHIBI
# ==========================================================

PASTA_CHIBI = "objetos/chibi/"

ARQUIVO_OBJ_CHIBI = PASTA_CHIBI + "chibi.obj"

ARQUIVO_TEX_CHIBI = PASTA_CHIBI + "chibi.png"


# ==========================================================
# OBJETO CAT
# ==========================================================

PASTA_CAT = "objetos/cat/"

ARQUIVO_OBJ_CAT = PASTA_CAT + "cat.obj"

ARQUIVO_TEX_CAT = PASTA_CAT + "cat_diffuse.jpg"


# ==========================================================
# CONFIGURAÇÕES DA JANELA
# ==========================================================

WIDTH = 800

HEIGHT = 600


# ==========================================================
# VARIÁVEIS GLOBAIS
# ==========================================================

# janela GLFW
Window = None

# shader principal
Shader_programm = None


# ==========================================================
# CHIBI
# ==========================================================

# VAO chibi
vao_chibi = None

# quantidade vértices
num_vertices_chibi = 0

# textura
textura_chibi = None


# ==========================================================
# CAT
# ==========================================================

# VAO gato
vao_cat = None

# quantidade vértices
num_vertices_cat = 0

# textura gato
textura_cat = None


# ==========================================================
# CÂMERA
# ==========================================================

cam = Camera()


# ==========================================================
# VARIÁVEIS MOUSE
# ==========================================================

# primeira leitura
first_mouse = True

# posição inicial mouse
lastX = WIDTH / 2

lastY = HEIGHT / 2


# ==========================================================
# CALLBACK REDIMENSIONAMENTO
# ==========================================================

def redimensiona_callback(window, w, h):

    """
    Executado quando janela muda tamanho.
    """

    global WIDTH
    global HEIGHT

    WIDTH = w

    HEIGHT = h

    # ajusta viewport OpenGL
    glViewport(0, 0, WIDTH, HEIGHT)


# ==========================================================
# CALLBACK TECLADO
# ==========================================================

def teclado_callback(window, key, scancode, action, mods):

    """
    Fecha aplicação ao pressionar ESC.
    """

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:

        glfw.set_window_should_close(window, True)


# ==========================================================
# CALLBACK MOUSE
# ==========================================================

def mouse_callback(window, xpos, ypos):

    """
    Controla rotação câmera com mouse.
    """

    global first_mouse

    global lastX
    global lastY

    # evita movimento brusco inicial
    if first_mouse:

        lastX = xpos

        lastY = ypos

        first_mouse = False

    # deslocamento horizontal
    xoffset = xpos - lastX

    # deslocamento vertical
    yoffset = lastY - ypos

    # atualiza posição
    lastX = xpos

    lastY = ypos

    # envia para câmera
    cam.process_mouse_movement(xoffset, yoffset)


# ==========================================================
# INICIALIZA OPENGL
# ==========================================================

def inicializa_opengl():

    """
    Inicializa:
    - GLFW
    - Janela
    - OpenGL
    """

    global Window

    # inicializa GLFW
    if not glfw.init():

        raise RuntimeError("Erro GLFW")

    # cria janela
    Window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "OpenGL Moderno",
        None,
        None
    )

    # verifica erro
    if not Window:

        glfw.terminate()

        raise RuntimeError("Erro Janela")

    # torna contexto OpenGL atual
    glfw.make_context_current(Window)

    # callbacks
    glfw.set_window_size_callback(
        Window,
        redimensiona_callback
    )

    glfw.set_key_callback(
        Window,
        teclado_callback
    )

    glfw.set_cursor_pos_callback(
        Window,
        mouse_callback
    )

    # captura mouse
    glfw.set_input_mode(
        Window,
        glfw.CURSOR,
        glfw.CURSOR_DISABLED
    )

    # ======================================================
    # DEPTH TEST
    # ======================================================

    # importante em cenas 3D
    #
    # evita objetos atrás aparecerem na frente

    glEnable(GL_DEPTH_TEST)

    # ======================================================
    # DESATIVA CULL FACE
    # ======================================================

    # alguns OBJ possuem faces invertidas
    #
    # evita objeto "furado"

    glDisable(GL_CULL_FACE)

    # mostra versão OpenGL
    print(glGetString(GL_VERSION).decode())


# ==========================================================
# CARREGA OBJETO
# ==========================================================

def carregar_objeto(arquivo_obj, arquivo_tex):

    """
    Carrega:
    - OBJ
    - VAO
    - VBO
    - textura
    """

    # ======================================================
    # CARREGA OBJ
    # ======================================================

    # retorna:
    #
    # buffer
    # quantidade vértices

    buffer, num_vertices = ObjLoaderSimple.load_obj(
        arquivo_obj
    )

    # converte para float32
    buffer = buffer.astype(np.float32)

    # ======================================================
    # CRIA VAO
    # ======================================================

    vao = glGenVertexArrays(1)

    # ativa VAO
    glBindVertexArray(vao)

    # ======================================================
    # CRIA VBO
    # ======================================================

    vbo = glGenBuffers(1)

    # ativa VBO
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # ======================================================
    # ENVIA BUFFER GPU
    # ======================================================

    glBufferData(
        GL_ARRAY_BUFFER,
        buffer.nbytes,
        buffer,
        GL_STATIC_DRAW
    )

    # ======================================================
    # CONFIGURA ATRIBUTOS
    # ======================================================

    # cada vértice:
    #
    # x y z u v

    stride = buffer.itemsize * 5

    # ======================================================
    # POSIÇÃO
    # ======================================================

    # ativa atributo posição
    glEnableVertexAttribArray(0)

    # configura leitura:
    #
    # x y z

    glVertexAttribPointer(
        0,                          # location shader
        3,                          # x y z
        GL_FLOAT,                  # tipo
        GL_FALSE,                  # normalizar
        stride,                    # tamanho vértice
        ctypes.c_void_p(0)         # offset
    )

    # ======================================================
    # UV
    # ======================================================

    # ativa atributo UV
    glEnableVertexAttribArray(1)

    # configura leitura:
    #
    # u v

    glVertexAttribPointer(
        1,                                  # location shader
        2,                                  # u v
        GL_FLOAT,                           # tipo
        GL_FALSE,                           # normalizar
        stride,                             # tamanho vértice
        ctypes.c_void_p(buffer.itemsize * 3)
    )

    # ======================================================
    # DESATIVA
    # ======================================================

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

    # ======================================================
    # TEXTURA
    # ======================================================

    textura = glGenTextures(1)

    load_texture(
        arquivo_tex,
        textura
    )

    return vao, num_vertices, textura


# ==========================================================
# SHADERS
# ==========================================================

def inicializa_shaders():

    """
    Cria shaders.
    """

    global Shader_programm

    # ======================================================
    # VERTEX SHADER
    # ======================================================

    vertex_src = """

        #version 400

        layout(location = 0) in vec3 in_pos;

        layout(location = 1) in vec2 in_uv;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        out vec2 frag_uv;

        void main()
        {
            frag_uv = in_uv;

            gl_Position =
                projection *
                view *
                model *
                vec4(in_pos, 1.0);
        }

    """

    # ======================================================
    # FRAGMENT SHADER
    # ======================================================

    fragment_src = """

        #version 400

        in vec2 frag_uv;

        uniform sampler2D texture1;

        out vec4 FragColor;

        void main()
        {
            FragColor = texture(texture1, frag_uv);
        }

    """

    # ======================================================
    # COMPILA VERTEX
    # ======================================================

    vertex_shader = OpenGL.GL.shaders.compileShader(
        vertex_src,
        GL_VERTEX_SHADER
    )

    # ======================================================
    # COMPILA FRAGMENT
    # ======================================================

    fragment_shader = OpenGL.GL.shaders.compileShader(
        fragment_src,
        GL_FRAGMENT_SHADER
    )

    # ======================================================
    # PROGRAMA FINAL
    # ======================================================

    Shader_programm = OpenGL.GL.shaders.compileProgram(
        vertex_shader,
        fragment_shader
    )


# ======================================================
# LOOP PRINCIPAL DA APLICAÇÃO
# ======================================================
#
# A partir deste ponto a aplicação entra
# em um loop contínuo de renderização.
#
# O render_loop():
#
# - processa teclado
# - processa mouse
# - atualiza câmera
# - limpa tela
# - desenha objetos
# - atualiza janela
#
# Esse loop permanece executando até
# o usuário fechar a aplicação.

# ======================================================
def render_loop():

    # ======================================================
    # MATRIZ MODEL - CHIBI
    # ======================================================

    # reduz tamanho chibi
    escala_chibi = pyrr.matrix44.create_from_scale(
        Vector3([0.4, 0.4, 0.4])
    )

    # move esquerda
    translacao_chibi = pyrr.matrix44.create_from_translation(
        Vector3([-2.0, 0.0, 0.0])
    )

    # aplica:
    #
    # escala
    # translação

    model_chibi = pyrr.matrix44.multiply(
        translacao_chibi,
        escala_chibi
    )

    # ======================================================
    # MATRIZ MODEL - GATO
    # ======================================================

    # aumenta gato
    escala_cat = pyrr.matrix44.create_from_scale(
        Vector3([0.12, 0.12, 0.12])
    )

    # coloca gato em pé
    rotacao_cat_x = pyrr.matrix44.create_from_x_rotation(
        np.radians(90)
    )

    # gira gato para frente
    #
    # removido problema dele olhar para trás

    rotacao_cat_y = pyrr.matrix44.create_from_y_rotation(
        np.radians(360)
    )

    # move gato lado do chibi
    #
    # mesmo eixo Z

    translacao_cat = pyrr.matrix44.create_from_translation(
        Vector3([15.5, -1.5, 0.0])
    )

    # ======================================================
    # MATRIZ FINAL GATO
    # ======================================================

    model_cat = pyrr.matrix44.multiply(
        rotacao_cat_x,
        escala_cat
    )

    model_cat = pyrr.matrix44.multiply(
        rotacao_cat_y,
        model_cat
    )

    model_cat = pyrr.matrix44.multiply(
        translacao_cat,
        model_cat
    )

    # ======================================================
    # CONTROLE TEMPO
    # ======================================================

    last_time = glfw.get_time()

    base_speed = 10.0

    # ======================================================
    # LOOP PRINCIPAL
    # ======================================================

    while not glfw.window_should_close(Window):

        # ==================================================
        # DELTA TIME
        # ==================================================

        current_time = glfw.get_time()

        delta = current_time - last_time

        last_time = current_time

        vel = base_speed * delta

        # ==================================================
        # MOVIMENTO CÂMERA
        # ==================================================

        if glfw.get_key(Window, glfw.KEY_W) == glfw.PRESS:

            cam.process_keyboard("FORWARD", vel)

        if glfw.get_key(Window, glfw.KEY_S) == glfw.PRESS:

            cam.process_keyboard("BACKWARD", vel)

        if glfw.get_key(Window, glfw.KEY_A) == glfw.PRESS:

            cam.process_keyboard("LEFT", vel)

        if glfw.get_key(Window, glfw.KEY_D) == glfw.PRESS:

            cam.process_keyboard("RIGHT", vel)

        # ==================================================
        # LIMPA TELA
        # ==================================================

        glClearColor(0.1, 0.1, 0.1, 1.0)

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        # ==================================================
        # ATIVA SHADER
        # ==================================================

        glUseProgram(Shader_programm)

        # ==================================================
        # VIEW
        # ==================================================

        view = cam.get_view_matrix()

        # ==================================================
        # PROJECTION
        # ==================================================

        projection = pyrr.matrix44.create_perspective_projection_matrix(
            45.0,
            WIDTH / HEIGHT,
            0.1,
            100.0
        )

        # ==================================================
        # ENVIA VIEW
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "view"),
            1,
            GL_FALSE,
            view
        )

        # ==================================================
        # ENVIA PROJECTION
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "projection"),
            1,
            GL_FALSE,
            projection
        )

        # ==================================================
        # DESENHA CHIBI
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_chibi
        )

        # ativa VAO
        glBindVertexArray(vao_chibi)

        # ativa textura
        glBindTexture(GL_TEXTURE_2D, textura_chibi)

        # desenha
        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_chibi
        )

        # ==================================================
        # DESENHA GATO
        # ==================================================

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_cat
        )

        # ativa VAO
        glBindVertexArray(vao_cat)

        # ativa textura
        glBindTexture(GL_TEXTURE_2D, textura_cat)

        # desenha
        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_cat
        )

        # ==================================================
        # ATUALIZA
        # ==================================================

        glfw.swap_buffers(Window)

        glfw.poll_events()

    glfw.terminate()


# ==========================================================
# MAIN
# ==========================================================

def main():

    global vao_chibi
    global num_vertices_chibi
    global textura_chibi

    global vao_cat
    global num_vertices_cat
    global textura_cat

    # inicializa OpenGL
    inicializa_opengl()

    # ======================================================
    # CHIBI
    # ======================================================

    vao_chibi, num_vertices_chibi, textura_chibi = carregar_objeto(
        ARQUIVO_OBJ_CHIBI,
        ARQUIVO_TEX_CHIBI
    )

    # ======================================================
    # GATO
    # ======================================================

    vao_cat, num_vertices_cat, textura_cat = carregar_objeto(
        ARQUIVO_OBJ_CAT,
        ARQUIVO_TEX_CAT
    )

    # shaders
    inicializa_shaders()

    # loop renderização
    render_loop()


# ==========================================================
# INÍCIO
# ==========================================================

if __name__ == "__main__":

    main()




# ==========================================================
# FLUXO GERAL DA APLICAÇÃO - EXPLICAÇÃO
# ==========================================================
#
# INÍCIO DO PROGRAMA
#
# if __name__ == "__main__":
#         ↓
#       main()
#
#
# ==========================================================
# MAIN
# ==========================================================
#
# main()
#
# 1) inicializa_opengl()
#       ↓
#    - GLFW
#    - janela
#    - callbacks
#    - OpenGL
#    - depth test
#
#
# 2) carregar_objeto(chibi.obj, chibi.png)
#       ↓
#    ObjLoaderSimple.load_obj()
#       ↓
#    - lê OBJ
#    - triangula faces
#    - cria buffer
#       ↓
#    OpenGL:
#    - cria VAO
#    - cria VBO
#    - envia buffer GPU
#       ↓
#    TextureLoader.load_texture()
#       ↓
#    - carrega imagem
#    - cria textura GPU
#
#
# 3) carregar_objeto(cat.obj, cat.jpg)
#       ↓
#    mesmo processo acima
#
#
# 4) inicializa_shaders()
#       ↓
#    - compila vertex shader
#    - compila fragment shader
#    - cria shader program
#
#
# 5) render_loop()
#       ↓
#    LOOP PRINCIPAL DA APLICAÇÃO
#
#
# ==========================================================
# RENDER LOOP
# ==========================================================
#
# enquanto janela aberta:
#
#   ↓
#
# 1) calcula delta time
#
# 2) processa teclado
#       ↓
#    movimenta câmera
#
# 3) processa mouse
#       ↓
#    atualiza yaw/pitch
#
# 4) limpa tela
#
# 5) ativa shader
#
# 6) cria matrizes:
#       ↓
#    - model
#    - view
#    - projection
#
# 7) envia matrizes GPU
#
# 8) desenha CHIBI
#       ↓
#    - ativa VAO
#    - ativa textura
#    - glDrawArrays()
#
# 9) desenha GATO
#       ↓
#    - ativa VAO
#    - ativa textura
#    - glDrawArrays()
#
# 10) atualiza janela
#       ↓
#    glfw.swap_buffers()
#
# 11) processa eventos
#       ↓
#    glfw.poll_events()
#
#
# ==========================================================
# FINALIZAÇÃO
# ==========================================================
#
# janela fechada:
#       ↓
# glfw.terminate()
#
# ==========================================================
