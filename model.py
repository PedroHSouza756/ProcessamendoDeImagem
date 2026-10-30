
# Importa a classe Image da biblioteca Pillow,
# utilizada para representar e manipular imagens.
from PIL import Image

# Importa o NumPy para realizar cálculos com matrizes
# e trabalhar com os valores dos pixels das imagens.
import numpy as np


# Filtro 1: converte a imagem para tons de cinza.
def escala_cinza(imagem):
    # O modo "L" representa uma imagem em escala de cinza.
    return imagem.convert("L")


# Função auxiliar para aplicar uma máscara 3x3 na imagem.
# É utilizada pelos filtros Blur e Sobel.
# Essa função serve para aplicar os filtros de matrizes na imagem
def convolucao(imagem, mascara):
    # Converte a imagem para cinza e transforma seus pixels em uma matriz de números decimais.
    pixels = np.array(imagem.convert("L"), dtype=np.float32)

    # Obtém a altura e a largura da imagem.
    altura, largura = pixels.shape

    # Adiciona uma borda de pixels ao redor da imagem.
    # O modo "edge" repete os valores dos pixels das extremidades.
    imagem_padded = np.pad(pixels, 1, mode="edge")

    # Cria uma matriz de zeros para armazenar o resultado.
    resultado = np.zeros((altura, largura), dtype=np.float32)

    # Percorre as três linhas da máscara.
    for i in range(3):

        # Percorre as três colunas da máscara.
        for j in range(3):

            # Multiplica cada posição da imagem pela posição
            # correspondente da máscara e soma ao resultado.
            resultado += (
                imagem_padded[i:i + altura, j:j + largura]
                * mascara[i, j]
            )

    # Retorna a matriz resultante da convolução.
    return resultado


# Filtro 2: Blur, utilizado para suavizar a imagem.
def blur(imagem):
    # Cria uma máscara 3x3 com nove valores iguais a 1/9.
    # Isso calcula a média dos pixels vizinhos.
    mascara = np.ones((3, 3), dtype=np.float32) / 9

    # Aplica a máscara de suavização na imagem.
    resultado = convolucao(imagem, mascara)

    # Limita os valores entre 0 e 255, converte para inteiros
    # de 8 bits e cria uma nova imagem em tons de cinza.
    # Converte a matriz de pixel em uma iamgem que pode ser salva ou exibida

    return Image.fromarray(
        np.clip(resultado, 0, 255).astype(np.uint8) # uint8 8bits sem sinal, numero inteiros, se for -10, será convertido para 0, 50.2 = 50
    )


# Filtro 3: Sobel, utilizado para detectar as bordas.

# Filtro 3: Sobel, utilizado para detectar as bordas.
def sobel(imagem):

    # Primeira máscara: detecta variações na direção vertical.
    mascara_y1 = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ], dtype=np.float32)

    # Segunda máscara: detecta variações na direção vertical.
    mascara_y2 = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ], dtype=np.float32)

    # Terceira máscara: detecta variações na direção horizontal.
    mascara_x1 = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ], dtype=np.float32)

    # Quarta máscara: detecta variações na direção horizontal.
    mascara_x2 = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    # Aplica as quatro máscaras à imagem.
    gy1 = convolucao(imagem, mascara_y1)
    gy2 = convolucao(imagem, mascara_y2)
    gx1 = convolucao(imagem, mascara_x1)
    gx2 = convolucao(imagem, mascara_x2)

    

    # Combina os resultados das duas direções.
    # Utiliza uma máscara de cada direção para calcular a magnitude.
    gx = (gx1 ** 2 + gx2 ** 2) / 2
    gy = (gy1 ** 2 + gy2 ** 2) / 2

    bordas = np.sqrt(gx + gy)

    # Limita os valores entre 0 e 255 e cria a imagem final.
    return Image.fromarray(
        np.clip(bordas, 0, 255).astype(np.uint8)
    )

# Filtro 4: Unsharp, conforme a fórmula do enunciado.
# Calcula a imagem original menos a imagem borrada.
def unsharp(imagem):
    # Converte a imagem original para cinza e utiliza inteiros de 16 bits para permitir resultados negativos.
    original = np.array(
        imagem.convert("L"), dtype=np.int16
    )

    # Aplica o Blur e transforma o resultado em uma matriz.
    borrada = np.array(
        blur(imagem), dtype=np.int16
    )

    # Subtrai a imagem borrada da imagem original.
    resultado = original - borrada

    # Limita os resultados entre 0 e 255.
    # Valores negativos são transformados em zero.
    return Image.fromarray(
        np.clip(resultado, 0, 255).astype(np.uint8)
    )


# Filtro 5: Sharpening, utilizado para realçar detalhes.
def sharpening(imagem):
    # Converte a imagem original para uma matriz em tons de cinza.
    original = np.array(
        imagem.convert("L"), dtype=np.int16
    )

    # Obtém os detalhes calculados pelo filtro Unsharp.
    detalhes = np.array(
        unsharp(imagem), dtype=np.int16
    )

    # Soma os detalhes à imagem original.
    resultado = original + detalhes

    # Limita os valores dos pixels entre 0 e 255.
    return Image.fromarray(
        np.clip(resultado, 0, 255).astype(np.uint8)
    )


# Função que seleciona qual filtro será executado.
# Recebe o nome do filtro e a imagem de entrada.
def aplicar_filtro(nome, imagem):

    # Dicionário que relaciona cada nome à sua função.
    filtros = {
        "Escala de cinza": escala_cinza,
        "Blur": blur,
        "Sobel": sobel,
        "Unsharp": unsharp,
        "Sharpening": sharpening
    }

    # Verifica se o nome recebido corresponde a um filtro.
    if nome not in filtros:
        raise ValueError("Filtro não reconhecido.")

    # Executa e retorna o resultado do filtro escolhido.
    return filtros[nome](imagem)