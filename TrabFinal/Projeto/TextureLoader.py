from OpenGL.GL import *

from PIL import Image

def load_texture(path,texture):
    glBindTexture(GL_TEXTURE_2D,texture)
    

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.convert("RGBA").tobytes()

    width, height = image.size

    glTexImage2D(
        GL_TEXTURE_2D,     # tipo textura
        0,                 # nível mipmap
        GL_RGBA,           # formato interno GPU
        width,             # largura imagem
        height,            # altura imagem
        0,                 # borda (não utilizado)
        GL_RGBA,           # formato imagem
        GL_UNSIGNED_BYTE,  # tipo dados
        image_data         # pixels imagem
    )

    glGenerateMipmap(GL_TEXTURE_2D)