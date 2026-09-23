from PIL import Image


def montar_histograma(imagem):
    histograma = [0] * 256
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            nivel = imagem.getpixel((x, y))
            histograma[nivel] += 1
    return histograma


def normalizar_histograma(histograma):
    total = sum(histograma)
    if total == 0:
        raise ValueError("A imagem deve conter pixels.")
    probabilidades = []
    for quantidade in histograma:
        probabilidades.append(quantidade / total)
    return probabilidades


def acumular_probabilidades(probabilidades):
    acumuladas = []
    soma = 0
    for probabilidade in probabilidades:
        soma += probabilidade
        acumuladas.append(soma)
    return acumuladas


def criar_lut(acumuladas, niveis=256):
    lut = []
    for probabilidade in acumuladas:
        lut.append(min(niveis - 1, int((niveis - 1) * probabilidade + 0.5)))
    return lut


def remapear_imagem(imagem, lut):
    largura, altura = imagem.size
    resultado = Image.new("L", imagem.size)
    for y in range(altura):
        for x in range(largura):
            resultado.putpixel((x, y), lut[imagem.getpixel((x, y))])
    return resultado


def equalizar_imagem(imagem):
    imagem = imagem.convert("L")
    histograma = montar_histograma(imagem)
    probabilidades = normalizar_histograma(histograma)
    acumuladas = acumular_probabilidades(probabilidades)
    lut = criar_lut(acumuladas)
    resultado = remapear_imagem(imagem, lut)
    return resultado, histograma, probabilidades, acumuladas, lut


def executar():
    caminho = input("Caminho da imagem: ").strip().strip('"')
    try:
        with Image.open(caminho) as entrada:
            resultado, histograma, probabilidades, acumuladas, lut = equalizar_imagem(entrada)
        resultado.save("equalizada.png")
        with open("histograma.csv", "w", encoding="utf-8") as arquivo:
            arquivo.write("nivel,frequencia,probabilidade,cdf,lut\n")
            for nivel in range(256):
                arquivo.write(f"{nivel},{histograma[nivel]},{probabilidades[nivel]},{acumuladas[nivel]},{lut[nivel]}\n")
        print("Imagem e tabela salvas na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
