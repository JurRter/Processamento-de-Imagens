from PIL import Image


def aplicar_media_padding_zeros(imagem):
    imagem = imagem.convert("L")
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    pixels = imagem.load()
    pixels_saida = resultado.load()
    for y in range(altura):
        for x in range(largura):
            soma = 0
            for deslocamento_y in range(-1, 2):
                for deslocamento_x in range(-1, 2):
                    vizinho_y = y + deslocamento_y
                    vizinho_x = x + deslocamento_x
                    if 0 <= vizinho_y < altura and 0 <= vizinho_x < largura:
                        soma += pixels[vizinho_x, vizinho_y]
            pixels_saida[x, y] = int(soma / 9 + 0.5)
    return resultado


def executar():
    caminho = input("Caminho da imagem: ").strip().strip('"')
    try:
        with Image.open(caminho) as entrada:
            resultado = aplicar_media_padding_zeros(entrada)
        resultado.save("media.png")
        print("Média salva na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
