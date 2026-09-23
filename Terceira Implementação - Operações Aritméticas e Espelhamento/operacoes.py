from PIL import Image


def somar_imagens(primeira, segunda):
    if primeira.size != segunda.size:
        raise ValueError("As imagens devem ter a mesma largura e altura.")
    primeira = primeira.convert("L")
    segunda = segunda.convert("L")
    largura, altura = primeira.size
    resultado = Image.new("L", primeira.size)
    for y in range(altura):
        for x in range(largura):
            soma = primeira.getpixel((x, y)) + segunda.getpixel((x, y))
            resultado.putpixel((x, y), min(255, soma))
    return resultado


def subtrair_imagens(primeira, segunda):
    if primeira.size != segunda.size:
        raise ValueError("As imagens devem ter a mesma largura e altura.")
    primeira = primeira.convert("L")
    segunda = segunda.convert("L")
    largura, altura = primeira.size
    resultado = Image.new("L", primeira.size)
    for y in range(altura):
        for x in range(largura):
            diferenca = primeira.getpixel((x, y)) - segunda.getpixel((x, y))
            resultado.putpixel((x, y), max(0, diferenca))
    return resultado


def espelhar_horizontal(imagem):
    imagem = imagem.convert("L")
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    for y in range(altura):
        for x in range(largura):
            resultado.putpixel((x, y), imagem.getpixel((largura - 1 - x, y)))
    return resultado


def executar():
    caminho_primeira = input("Caminho da primeira imagem: ").strip().strip('"')
    caminho_segunda = input("Caminho da segunda imagem: ").strip().strip('"')
    try:
        with Image.open(caminho_primeira) as entrada:
            primeira = entrada.convert("L")
        with Image.open(caminho_segunda) as entrada:
            segunda = entrada.convert("L")
        soma = somar_imagens(primeira, segunda)
        diferenca = subtrair_imagens(primeira, segunda)
        espelhada = espelhar_horizontal(primeira)
        soma.save("adicao.png")
        diferenca.save("subtracao.png")
        espelhada.save("espelhamento.png")
        print("Resultados salvos na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
