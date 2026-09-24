from PIL import Image


def aplicar_negativo(imagem):
    imagem = imagem.convert("L")
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    for y in range(altura):
        for x in range(largura):
            resultado.putpixel((x, y), 255 - imagem.getpixel((x, y)))
    return resultado


def executar():
    caminho = input("Caminho da imagem: ").strip().strip('"')
    try:
        with Image.open(caminho) as entrada:
            resultado = aplicar_negativo(entrada)
        resultado.save("negativo.png")
        print("Negativo salvo na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
