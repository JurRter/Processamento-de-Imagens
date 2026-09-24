from PIL import Image


MASCARAS_LAPLACIANO = {
    "a": [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
    "b": [[1, 1, 1], [1, -8, 1], [1, 1, 1]],
    "c": [[0, -1, 0], [-1, 4, -1], [0, -1, 0]],
    "d": [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
}
MASCARA_SOBEL_GX = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
MASCARA_SOBEL_GY = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def aplicar_mascara_padding_zeros(imagem, mascara):
    imagem = imagem.convert("L")
    largura, altura = imagem.size
    pixels = imagem.load()
    resposta = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            soma = 0
            for linha_mascara in range(3):
                for coluna_mascara in range(3):
                    vizinho_y = y + linha_mascara - 1
                    vizinho_x = x + coluna_mascara - 1
                    if 0 <= vizinho_y < altura and 0 <= vizinho_x < largura:
                        soma += pixels[vizinho_x, vizinho_y] * mascara[linha_mascara][coluna_mascara]
            linha.append(soma)
        resposta.append(linha)
    return resposta


def converter_com_saturacao(matriz):
    altura = len(matriz)
    largura = len(matriz[0])
    resultado = Image.new("L", (largura, altura))
    for y in range(altura):
        for x in range(largura):
            valor = max(0, min(255, int(matriz[y][x] + 0.5)))
            resultado.putpixel((x, y), valor)
    return resultado


def aplicar_sobel(imagem):
    gx = aplicar_mascara_padding_zeros(imagem, MASCARA_SOBEL_GX)
    gy = aplicar_mascara_padding_zeros(imagem, MASCARA_SOBEL_GY)
    magnitude = []
    for y in range(len(gx)):
        linha = []
        for x in range(len(gx[0])):
            linha.append((gx[y][x] ** 2 + gy[y][x] ** 2) ** 0.5)
        magnitude.append(linha)
    return gx, gy, magnitude


def salvar_matriz(matriz, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for linha in matriz:
            arquivo.write(",".join(str(valor) for valor in linha) + "\n")


def executar():
    caminho = input("Caminho da imagem: ").strip().strip('"')
    try:
        with Image.open(caminho) as entrada:
            imagem = entrada.convert("L")
        for nome, mascara in MASCARAS_LAPLACIANO.items():
            resposta = aplicar_mascara_padding_zeros(imagem, mascara)
            converter_com_saturacao(resposta).save("laplaciano_" + nome + ".png")
            salvar_matriz(resposta, "laplaciano_" + nome + ".csv")
        gx, gy, magnitude = aplicar_sobel(imagem)
        for nome, resposta in [("sobel_gx", gx), ("sobel_gy", gy), ("sobel_magnitude", magnitude)]:
            converter_com_saturacao(resposta).save(nome + ".png")
            salvar_matriz(resposta, nome + ".csv")
        print("Imagens e respostas numéricas salvas na pasta de execução.")
    except (OSError, ValueError) as erro:
        print("Erro:", erro)
        raise SystemExit(1)


if __name__ == "__main__":
    executar()
