# Importação das bibliotecas necessárias
import pygame                                # Responsável por criar a janela e capturar entrada do teclado
from pygame.locals import *                  # Importa constantes úteis do pygame (como teclas)
from OpenGL.GL import *                      # Comandos do OpenGL para renderização (ex: glBegin, glVertex, glEnable)
from OpenGL.GLU import *                     # Comandos utilitários do OpenGL (ex: gluPerspective, gluLookAt)
from PIL import Image                        # Usada para abrir e processar imagens para texturas

# Variáveis globais de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -10     # Define a posição inicial da câmera (afastada no eixo Z)
rot_x, rot_y = 0, 0                          # Ângulos de rotação da câmera (x para inclinar, y para girar)

# Função que carrega uma imagem e a transforma em textura OpenGL
def load_texture(filename):
    img = Image.open(filename)               # Abre a imagem com Pillow
    img = img.transpose(Image.FLIP_TOP_BOTTOM) # Inverte verticalmente (OpenGL considera origem no canto inferior)
    img_data = img.convert("RGBA").tobytes() # Converte a imagem para bytes RGBA
    width, height = img.size                 # Obtém tamanho da imagem
    tex_id = glGenTextures(1)                # Gera um novo ID de textura
    glBindTexture(GL_TEXTURE_2D, tex_id)     # Ativa o ID gerado para as próximas operações
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data) # Cria a textura
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Repetir horizontalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # Repetir verticalmente
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # Suavizar ao ampliar
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Suavizar ao reduzir
    return tex_id                            # Retorna o ID da textura para uso posterior

# Função que desenha um cubo com textura aplicada, face por face
def draw_textured_cube():
    glBegin(GL_QUADS)                        # Inicia desenho de quadriláteros

    # FACE TRASEIRA (fundo do cubo)
    glNormal3f(0.0, 0.0, -1.0)               # [QUESTÃO 05] Define a direção da face para a luz (trás)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0]) # Mapeia textura no vértice inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1]) # Mapeia textura no vértice inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[2]) # Mapeia textura no vértice superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[3]) # Mapeia textura no vértice superior esquerdo

    # FACE FRONTAL (frente do cubo)
    glNormal3f(0.0, 0.0, 1.0)                # [QUESTÃO 05] Define a direção da face para a luz (frente)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[4]) # Vértice inferior esquerdo
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[5]) # Vértice inferior direito
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6]) # Vértice superior direito
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7]) # Vértice superior esquerdo

    # FACE INFERIOR (base)
    glNormal3f(0.0, -1.0, 0.0)               # [QUESTÃO 05] Define a direção da face para a luz (baixo)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0]) # Traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[1]) # Traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[5]) # Frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4]) # Frontal esquerda

    # FACE SUPERIOR (tampa)
    glNormal3f(0.0, 1.0, 0.0)                # [QUESTÃO 05] Define a direção da face para a luz (cima)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[3]) # Traseira esquerda
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2]) # Traseira direita
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6]) # Frontal direita
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[7]) # Frontal esquerda

    # FACE DIREITA (lado direito do cubo)
    glNormal3f(1.0, 0.0, 0.0)                # [QUESTÃO 05] Define a direção da face para a luz (direita)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[1]) # Inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[2]) # Superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[6]) # Superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[5]) # Inferior frontal

    # FACE ESQUERDA (lado esquerdo do cubo)
    glNormal3f(-1.0, 0.0, 0.0)               # [QUESTÃO 05] Define a direção da face para a luz (esquerda)
    glTexCoord2f(0, 0); glVertex3fv(cube_vertices[0]) # Inferior traseiro
    glTexCoord2f(1, 0); glVertex3fv(cube_vertices[3]) # Superior traseiro
    glTexCoord2f(1, 1); glVertex3fv(cube_vertices[7]) # Superior frontal
    glTexCoord2f(0, 1); glVertex3fv(cube_vertices[4]) # Inferior frontal

    glEnd()                                  # Finaliza o desenho das faces

# Lista de coordenadas 3D dos vértices do cubo
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

# Função para configurar o ambiente OpenGL
# Função para configurar o ambiente OpenGL
def init_opengl(display):
    glEnable(GL_DEPTH_TEST)                  # Ativa o teste de profundidade (3D real)
    glEnable(GL_TEXTURE_2D)                  # Ativa o uso de texturas nos objetos
    glEnable(GL_LIGHTING)                    # Ativa o sistema de cálculo de luz
    glEnable(GL_LIGHT0)                      # Ativa a fonte de luz número 0

    # SOLUÇÃO PARA O MURO: Ativa a cor do material para seguir a textura sem escurecer
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # [QUESTÃO 04] Altera GL_LIGHT_MODEL_AMBIENT para um tom azulado (clareado para iluminar o muro)
    # Valores (R, G, B, A). O 0.6 e 0.9 garantem que o "escuro" seja um azul bem claro.
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.6, 0.6, 0.9, 1.0)) 

    # [QUESTÃO 05] Configurações da luz principal (Lâmpada forte)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Cor difusa (Branco puro)
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0)) # Brilho especular (Reflexo branco)

    # Configurações de reflexão do material (exigido para brilho especular em alguns drivers)
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0)) 
    glMaterialf(GL_FRONT, GL_SHININESS, 80)  # Fator de brilho/polimento do material

    glMatrixMode(GL_PROJECTION)              # Muda para matriz de projeção (ajuste da lente)
    glLoadIdentity()                         # Reseta a matriz para evitar distorções
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) # Define FOV e planos de corte
    glMatrixMode(GL_MODELVIEW)               # Volta para matriz de modelo (posicionamento de objetos)




# Função principal do programa
def main():
    pygame.init()                            # Inicializa o Pygame
    display = (800, 600)                     # Define tamanho da janela
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL) # Cria janela OpenGL

    init_opengl(display)                     # Configura OpenGL
    
    # [QUESTÃO 01] Carrega diferentes texturas
    tex_caixa = load_texture("texturas/caixa.jpg")    # Textura para o cubo principal
    tex_grama = load_texture("texturas/grama.jpg")    # Textura para o chão (Q02)
    tex_parede = load_texture("texturas/parede.jpg")  # Textura para a parede (Q03)
    tex_madeira = load_texture("texturas/madeira.jpg") # Textura para o totem (Q06)

    clock = pygame.time.Clock()              # Relógio para frames
    global camera_x, camera_y, camera_z, rot_x, rot_y # Variáveis de controle

    running = True                           # Controle do loop
    while running:                           # Inicia loop principal
        clock.tick(60)                       # Limita a 60 FPS
        for event in pygame.event.get():     # Captura eventos
            if event.type == pygame.QUIT:    # Se fechar a janela
                running = False              # Para o programa

        keys = pygame.key.get_pressed()      # Captura teclas
        if keys[K_w]: camera_z += 0.1        # Move para frente
        if keys[K_s]: camera_z -= 0.1        # Move para trás
        if keys[K_a]: camera_x += 0.1        # Move para esquerda
        if keys[K_d]: camera_x -= 0.1        # Move para direita
        if keys[K_q]: rot_y -= 1             # Gira para esquerda
        if keys[K_e]: rot_y += 1             # Gira para direita
        if keys[K_r]: rot_x -= 1             # Inclina para cima
        if keys[K_f]: rot_x += 1             # Inclina para baixo

        target_x, target_y, target_z = camera_x, camera_y, camera_z + 1 # Define alvo da câmera
        glLoadIdentity()                     # Reseta a matriz
        gluLookAt(
            camera_x, camera_y, camera_z,  # 1. POSIÇÃO DO "OLHO" (Onde a câmera está no mundo)
            target_x, target_y, target_z,  # 2. PONTO DE ALVO (Para onde a lente está apontada)
            0, 1, 0                        # 3. VETOR "UP" (Onde é o 'cima' do mundo - Eixo Y positivo)
        )

        # [QUESTÃO 05 - RESOLUÇÃO] - Lâmpada posicionada logo após o gluLookAt
        # Isso faz com que a luz venha de "cima e de trás" da câmera, iluminando tudo à frente
        glLightfv(
            GL_LIGHT0,    # 1. QUAL LUZ (O OpenGL permite várias, de LIGHT0 até LIGHT7)
            GL_POSITION,  # 2. O QUE DEFINIR (Neste caso, estamos definindo a Posição/Direção)
            (0, 10, -10, 0) # 3. COORDENADAS (X, Y, Z, W)
            )
        '''0 (W - O parâmetro crucial):
                Quando é 0, as coordenadas anteriores funcionam como um VETOR DE DIREÇÃO (Luz Direcional). 
                A luz não tem um ponto de origem, ela simplesmente "corre" naquela direção, como o Sol.
                Se fosse 1, seria uma Luz Posicional (Lâmpada), que brilha a partir de um ponto específico e perde força com a distância.'''
        

        glRotatef(rot_x, 1, 0, 0)            # Aplica rotação X
        glRotatef(rot_y, 0, 1, 0)            # Aplica rotação Y

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa a tela

        # [QUESTÃO 07] Montagem da Cena
        
        # [QUESTÃO 02] Desenha o CHÃO (Grama)
        glPushMatrix()                       # Salva estado atual
        glBindTexture(GL_TEXTURE_2D, tex_grama) # Ativa textura de grama
        glTranslatef(0, -2, 0)               # Move para y = -2
        glScalef(10, 0.1, 10)                # Achata para parecer um piso
        draw_textured_cube()                 # Desenha o chão
        glPopMatrix()                        # Restaura estado

        # [QUESTÃO 03] Desenha a PAREDE (Tijolo)
        glPushMatrix()                       # Salva estado
        glBindTexture(GL_TEXTURE_2D, tex_parede) # Ativa textura de parede
        glTranslatef(0, 1, 8)                # Posiciona atrás do cubo principal
        glScalef(10, 3, 0.1)                 # Deixa alta e fina como um muro
        draw_textured_cube()                 # Desenha a parede
        glPopMatrix()                        # Restaura estado

        # [QUESTÃO 06] Desenha o TOTEM (3 cubos empilhados)
        for i in range(3):                   # Loop para criar 3 cubos
            glPushMatrix()                   # Salva estado
            glBindTexture(GL_TEXTURE_2D, tex_madeira) # Usa textura de madeira
            glTranslatef(-4, -1 + (i * 2), 0) # Empilha no eixo Y na esquerda
            draw_textured_cube()             # Desenha cada bloco do totem
            glPopMatrix()                    # Restaura estado

        # CUBO PRINCIPAL (Posicionado à direita do totem)
        glPushMatrix()                       # Salva estado
        glBindTexture(GL_TEXTURE_2D, tex_caixa) # Ativa textura do cubo
        glTranslatef(2, 0, 0)                # Move para a direita
        draw_textured_cube()                 # Desenha o cubo principal
        glPopMatrix()                        # Restaura estado

        pygame.display.flip()                # Renderiza o frame

    pygame.quit()                            # Finaliza o Pygame

if __name__ == "__main__":                   # Ponto de entrada
    main()                                   # Chama a função principal