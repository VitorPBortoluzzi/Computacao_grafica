import glfw

from OpenGL.GL import *
import OpenGL.GL.shaders

import numpy as np

import pyrr
from pyrr import Vector3

import ctypes

from TextureLoader import load_texture

from Camera import Camera

from Obj_Loader import ObjLoaderSimple



# ==========================================================
# OBJETOS \/ \/ \/ \/ \/
# ==========================================================

#Casa
vao_house = None

num_vertices_house = 0

textura_house = None

#Cubo
vao_cubo = None
num_vertices_cubo = 0
textura_cubo = None


# ==========================================================
# CONFIGURAÇÕES DA JANELA
# ==========================================================


WIDTH = 1200

HEIGHT = 800

# ==========================================================

Window = None

Shader_programm = None



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

def carregar_objeto(arquivo_obj, arquivo_tex):

    buffer, num_vertices = ObjLoaderSimple.load_obj(
        arquivo_obj
    )

    buffer = buffer.astype(np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        buffer.nbytes,
        buffer,
        GL_STATIC_DRAW
    )

    stride = buffer.itemsize * 5

    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(1)

    glVertexAttribPointer(
        1,
        2,
        GL_FLOAT,
        GL_FALSE,
        stride,
        ctypes.c_void_p(buffer.itemsize * 3)
    )

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    textura = glGenTextures(1)

    load_texture(
        arquivo_tex,
        textura
    )

    return vao, num_vertices, textura

def criar_cubo():
    vertices_cubo = np.array([

        # Frente
        -0.5,-0.5, 0.5, 0.0,0.0,
        0.5,-0.5, 0.5, 1.0,0.0,
        0.5, 0.5, 0.5, 1.0,1.0,

        0.5, 0.5, 0.5, 1.0,1.0,
        -0.5, 0.5, 0.5, 0.0,1.0,
        -0.5,-0.5, 0.5, 0.0,0.0,

        # Trás
        -0.5,-0.5,-0.5, 1.0,0.0,
        -0.5, 0.5,-0.5, 1.0,1.0,
        0.5, 0.5,-0.5, 0.0,1.0,

        0.5, 0.5,-0.5, 0.0,1.0,
        0.5,-0.5,-0.5, 0.0,0.0,
        -0.5,-0.5,-0.5, 1.0,0.0,

        # Esquerda
        -0.5, 0.5, 0.5, 1.0,1.0,
        -0.5, 0.5,-0.5, 0.0,1.0,
        -0.5,-0.5,-0.5, 0.0,0.0,

        -0.5,-0.5,-0.5, 0.0,0.0,
        -0.5,-0.5, 0.5, 1.0,0.0,
        -0.5, 0.5, 0.5, 1.0,1.0,

        # Direita
        0.5, 0.5, 0.5, 0.0,1.0,
        0.5,-0.5,-0.5, 1.0,0.0,
        0.5, 0.5,-0.5, 1.0,1.0,

        0.5,-0.5,-0.5, 1.0,0.0,
        0.5, 0.5, 0.5, 0.0,1.0,
        0.5,-0.5, 0.5, 0.0,0.0,

        # Topo
        -0.5, 0.5,-0.5, 0.0,1.0,
        -0.5, 0.5, 0.5, 0.0,0.0,
        0.5, 0.5, 0.5, 1.0,0.0,

        0.5, 0.5, 0.5, 1.0,0.0,
        0.5, 0.5,-0.5, 1.0,1.0,
        -0.5, 0.5,-0.5, 0.0,1.0,

        # Base
        -0.5,-0.5,-0.5, 1.0,1.0,
        0.5,-0.5, 0.5, 0.0,0.0,
        -0.5,-0.5, 0.5, 1.0,0.0,

        0.5,-0.5, 0.5, 0.0,0.0,
        -0.5,-0.5,-0.5, 1.0,1.0,
        0.5,-0.5,-0.5, 0.0,1.0,

    ], dtype=np.float32)

    vao_cubo = glGenVertexArrays(1)
    glBindVertexArray(vao_cubo)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices_cubo.nbytes,
        vertices_cubo,
        GL_STATIC_DRAW
    )

    stride = 5 * 4

    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE,
        stride, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1, 2, GL_FLOAT, GL_FALSE,
        stride, ctypes.c_void_p(12)
    )
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    textura_cubo = glGenTextures(1)

    load_texture(
        "objetos/texture/Grass005_1K-JPG_Color.jpg",
        textura_cubo
    )

    num_vertices_cubo = 36
    
    return vao_cubo, num_vertices_cubo, textura_cubo

#=======================================
#Shaders================================
#=======================================
def inicializa_shaders():

    global Shader_programm

    vertex_src = """

    #version 330 core

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
            vec4(in_pos,1.0);
    }
    """

    fragment_src = """

    #version 330 core

    in vec2 frag_uv;

    uniform sampler2D texture1;

    out vec4 FragColor;

    void main()
    {
        FragColor =
            texture(texture1, frag_uv);
    }
    """
    vertex_shader = OpenGL.GL.shaders.compileShader(
        vertex_src,
        GL_VERTEX_SHADER
    )

    fragment_shader = OpenGL.GL.shaders.compileShader(
        fragment_src,
        GL_FRAGMENT_SHADER
    )

    Shader_programm = OpenGL.GL.shaders.compileProgram(
        vertex_shader,
        fragment_shader
    )




def render_loop():

    
    # casas
    escala_house = pyrr.matrix44.create_from_scale(
        Vector3([1.0, 1.0, 1.0])
    )

    rotacao_house = pyrr.matrix44.create_from_y_rotation(
        np.radians(25)
    )

    translacao_house = pyrr.matrix44.create_from_translation(
        Vector3([-85.0, 0.0, -34.0])
    )

    model_house = pyrr.matrix44.multiply(
        rotacao_house,
        escala_house
    )

    model_house = pyrr.matrix44.multiply(
        translacao_house,
        model_house
    )

    rotacao_house2 = pyrr.matrix44.create_from_y_rotation(
        np.radians(-75)
    )

    translacao_house2 = pyrr.matrix44.create_from_translation(
        Vector3([25.0, 0.0, 45.0])
    )

    model_house2 = pyrr.matrix44.multiply(
        rotacao_house2,
        escala_house
    )

    model_house2 = pyrr.matrix44.multiply(
        translacao_house2,
        model_house2
    )

    rotacao_house3 = pyrr.matrix44.create_from_y_rotation(
        np.radians(-35)
    )

    translacao_house3 = pyrr.matrix44.create_from_translation(
        Vector3([-25.0, 0.0, 70.0])
    )

    model_house3 = pyrr.matrix44.multiply(
        rotacao_house3,
        escala_house
    )

    model_house3 = pyrr.matrix44.multiply(
        translacao_house3,
        model_house3
    )

    escala_cubo = pyrr.matrix44.create_from_scale(
    Vector3([500.0, 0.3, 500.0])
    )

    translacao_cubo = pyrr.matrix44.create_from_translation(
        Vector3([0.0, -1.0, 0.0])
    )

    model_cubo = pyrr.matrix44.multiply(
        translacao_cubo,
        escala_cubo
    )

    
    # ======================================================
    # CONTROLE TEMPO
    # ======================================================

    last_time = glfw.get_time()

    ultimo_print = glfw.get_time()

    base_speed = 25.0

    # ======================================================
    # LOOP PRINCIPAL
    # ======================================================

    while not glfw.window_should_close(Window):

        # ==================================================
        # DELTA TIME
        # ==================================================

        current_time = glfw.get_time()

        if current_time - ultimo_print >= 5.0:

            print(
                "Camera:",
                cam.camera_pos.x,
                cam.camera_pos.y,
                cam.camera_pos.z
            )

            ultimo_print = current_time

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
            600.0
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

        #Casas

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_house
        )

        glBindVertexArray(vao_house)

        glBindTexture(
            GL_TEXTURE_2D,
            textura_house
        )

        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_house
        )

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_house2
        )

        glBindVertexArray(vao_house)

        glBindTexture(
            GL_TEXTURE_2D,
            textura_house
        )

        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_house
        )

#casa 3

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_house3
        )

        glBindVertexArray(vao_house)
        glBindTexture(GL_TEXTURE_2D, textura_house)

        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_house
        )

        glUniformMatrix4fv(
            glGetUniformLocation(Shader_programm, "model"),
            1,
            GL_FALSE,
            model_cubo
        )

        glBindVertexArray(vao_cubo)

        glBindTexture(
            GL_TEXTURE_2D,
            textura_cubo
        )

        glDrawArrays(
            GL_TRIANGLES,
            0,
            num_vertices_cubo
        )

        arvores = [
            (-30, 0, -20),
            (-10, 0, 40),
            (-7,0,-10),
            (50, 0, 60),
            (-45, 0, 15),
            (-25, 0, -35),
            (-15, 0, 5),
            (-2, 0, 50),
            (12, 0, 30),
            (18, 0, -40),
            (28, 0, 10),
            (33, 0, 45),
            (37, 0, -5),
            (42, 0, -30),
            (48, 0, 22),
            (-38, 0, -50),
            (60, 0, 5),
            (-70, 0, 10),
            (-55, 0, 35),
            (-60, 0, -15),
            
            (-20, 0, 80),
            (0, 0, 85),
            (65, 0, 70),
            
            (-40, 0, -60),
            (-15, 0, -55),
            (10, 0, -65),
            (45, 0, -50),
            
            (75, 0, 20),
            (68, 0, -35),
            (80, 0, 45),
            
            (-35, 0, 30),
            (-22, 0, -5),
            (15, 0, 5),
            (30, 0, -30),
            (35, 0, 25),
            (40, 0, 50),
            (52, 0, -5),
            (-5, 0, -30)
        ]

        for x, y, z in arvores:

            # =====================
            # Tronco
            # =====================

            escala_tronco = pyrr.matrix44.create_from_scale(
                Vector3([1.0, 6.0, 1.0])
            )

            translacao_tronco = pyrr.matrix44.create_from_translation(
                Vector3([x, 0.5, z])
            )

            model_tronco = pyrr.matrix44.multiply(
                translacao_tronco,
                escala_tronco
            )

            glUniformMatrix4fv(
                glGetUniformLocation(Shader_programm, "model"),
                1,
                GL_FALSE,
                model_tronco
            )

            glBindVertexArray(vao_cubo)

            glBindTexture(
                GL_TEXTURE_2D,
                textura_tronco
            )

            glDrawArrays(
                GL_TRIANGLES,
                0,
                num_vertices_cubo
            )

            # =====================
            # Copa
            # =====================

            escala_copa = pyrr.matrix44.create_from_scale(
                Vector3([5.0, 10.0, 5.0])
            )

            translacao_copa = pyrr.matrix44.create_from_translation(
                Vector3([x*0.2, 1, z*0.2])
            )

            model_copa = pyrr.matrix44.multiply(
                translacao_copa,
                escala_copa
            )

            glUniformMatrix4fv(
                glGetUniformLocation(Shader_programm, "model"),
                1,
                GL_FALSE,
                model_copa
            )

            glBindTexture(
                GL_TEXTURE_2D,
                textura_folhas
            )

            glDrawArrays(
                GL_TRIANGLES,
                0,
                num_vertices_cubo
            )
        # ==================================================
        # ATUALIZA
        # ==================================================

        glfw.swap_buffers(Window)

        glfw.poll_events()

    glfw.terminate()

def main():

    global vao_house
    global num_vertices_house
    global textura_house

    global vao_cubo,num_vertices_cubo,textura_cubo 

    global textura_tronco
    global textura_folhas

    inicializa_opengl()

    vao_cubo,num_vertices_cubo,textura_cubo = criar_cubo()

    vao_house, num_vertices_house, textura_house = carregar_objeto(
    "objetos/house/farmhouse_obj.obj",
    "objetos/house/Farmhouse Texture.jpg"
    )

    textura_tronco = glGenTextures(1)
    load_texture(
        "objetos/texture/tronco.jpg",
        textura_tronco
    )

    textura_folhas = glGenTextures(1)
    load_texture(
        "objetos/texture/folhas.jpg",
        textura_folhas
    )

    inicializa_shaders()

    render_loop()

if __name__ == "__main__":
    main()