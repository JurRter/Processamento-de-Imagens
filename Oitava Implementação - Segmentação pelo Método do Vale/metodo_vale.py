from PIL import Image


def montar_histograma(imagem):
    histograma = [0] * 256
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            nivel = imagem.getpixel((x, y))
            histograma[nivel] += 1
    return histograma


def encontrar_limiar(histograma):
    if sum(histograma) == 0:
        raise ValueError("A imagem deve conter pixels.")

    melhor_limiar = None
    menor_distancia = 256
    inicio = 1

    while inicio < 255:
        fim = inicio
        while fim < 254 and histograma[fim + 1] == histograma[inicio]:
            fim += 1

        if histograma[inicio] < histograma[inicio - 1] and histograma[fim] < histograma[fim + 1]:
            limiar = max(inicio, min(128, fim))
            distancia = abs(limiar - 128)
            if distancia < menor_distancia:
                melhor_limiar = limiar
                menor_distancia = distancia

        inicio = fim + 1

    if melhor_limiar is None:
        raise ValueError("Não foi encontrado um vale no histograma.")

    return melhor_limiar


def segmentar_imagem(imagem):
    imagem = imagem.convert("L")
    histograma = montar_histograma(imagem)
    limiar = encontrar_limiar(histograma)
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)

    for y in range(altura):
        for x in range(largura):
            if imagem.getpixel((x, y)) > limiar:
                resultado.putpixel((x, y), 255)
            else:
                resultado.putpixel((x, y), 0)

    return resultado, histograma, limiar


def executar():
    caminho = input("Caminho da imagem: ").strip().strip('"')
    try:
        with Image.open(caminho) as entrada:
            resultado, histograma, limiar = segmentar_imagem(entrada)

        resultado.save("segmentada.png")
        with open("histograma.csv", "w", encoding="utf-8") as arquivo:
            arquivo.write("nivel,frequencia\n")
            for nivel in range(256):
                arquivo.write(f"{nivel},{histograma[nivel]}\n")

        print("Limiar encontrado:", limiar)
        print("Imagem e histograma salvos na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
