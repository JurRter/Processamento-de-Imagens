from pathlib import Path
from PIL import Image


def binarizar_imagem(imagem):
    imagem = imagem.convert("L")
    resultado = Image.new("L", imagem.size)
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            if imagem.getpixel((x, y)) > 127:
                resultado.putpixel((x, y), 255)
    return resultado


def aplicar_erosao(imagem):
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    pixels = imagem.load()
    pixels_saida = resultado.load()
    for y in range(altura):
        for x in range(largura):
            valor = 255
            for deslocamento_y in range(-1, 2):
                for deslocamento_x in range(-1, 2):
                    vizinho_x = x + deslocamento_x
                    vizinho_y = y + deslocamento_y
                    if not (0 <= vizinho_x < largura and 0 <= vizinho_y < altura):
                        valor = 0
                    elif pixels[vizinho_x, vizinho_y] == 0:
                        valor = 0
            pixels_saida[x, y] = valor
    return resultado


def aplicar_dilatacao(imagem):
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    pixels = imagem.load()
    pixels_saida = resultado.load()
    for y in range(altura):
        for x in range(largura):
            valor = 0
            for deslocamento_y in range(-1, 2):
                for deslocamento_x in range(-1, 2):
                    vizinho_x = x + deslocamento_x
                    vizinho_y = y + deslocamento_y
                    if 0 <= vizinho_x < largura and 0 <= vizinho_y < altura:
                        if pixels[vizinho_x, vizinho_y] == 255:
                            valor = 255
            pixels_saida[x, y] = valor
    return resultado


def executar():
    pasta = Path(__file__).resolve().parent
    caminho = input("Caminho da imagem (Enter para imagem_teste.png): ").strip().strip('"')
    if not caminho:
        caminho = pasta / "imagem_teste.png"
    try:
        with Image.open(caminho) as entrada:
            binaria = binarizar_imagem(entrada)
        erodida = aplicar_erosao(binaria)
        dilatada = aplicar_dilatacao(binaria)
        pasta_saida = pasta / "resultados"
        pasta_saida.mkdir(exist_ok=True)
        binaria.save(pasta_saida / "binaria.png")
        erodida.save(pasta_saida / "erosao.png")
        dilatada.save(pasta_saida / "dilatacao.png")
        print("Elemento estruturante: quadrado 3 x 3, com origem no centro.")
        print("Objeto branco e fundo preto. Fora da imagem é considerado fundo.")
        print("Resultados salvos em:", pasta_saida)
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
