from PIL import Image
import random

def rotular_imagem(caminho_entrada, caminho_saida):
    imagem = Image.open(caminho_entrada).convert('L')
    largura, altura = imagem.size
    pixels = imagem.load()
    
    matriz = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            if pixels[x, y] > 127:
                linha.append(1)
            else:
                linha.append(0)
        matriz.append(linha)
        
    rotulos = []
    for y in range(altura):
        linha_rotulos = [0] * largura
        rotulos.append(linha_rotulos)
        
    proximo_rotulo = 1
    equivalencias = [0]
    
    for y in range(altura):
        for x in range(largura):
            if matriz[y][x] == 1:
                r = rotulos[y][x-1] if x > 0 else 0
                s = rotulos[y-1][x] if y > 0 else 0
                
                if r == 0 and s == 0:
                    rotulos[y][x] = proximo_rotulo
                    equivalencias.append(proximo_rotulo)
                    proximo_rotulo += 1
                elif r > 0 and s == 0:
                    rotulos[y][x] = r
                elif r == 0 and s > 0:
                    rotulos[y][x] = s
                else:
                    rotulos[y][x] = r
                    
                    atual_r = r
                    while equivalencias[atual_r] != atual_r:
                        atual_r = equivalencias[atual_r]
                        
                    atual_s = s
                    while equivalencias[atual_s] != atual_s:
                        atual_s = equivalencias[atual_s]
                        
                    if atual_r != atual_s:
                        menor = min(atual_r, atual_s)
                        maior = max(atual_r, atual_s)
                        equivalencias[maior] = menor

    for y in range(altura):
        for x in range(largura):
            if rotulos[y][x] > 0:
                atual = rotulos[y][x]
                while equivalencias[atual] != atual:
                    atual = equivalencias[atual]
                rotulos[y][x] = atual
                
    cores = {}
    imagem_saida = Image.new('RGB', (largura, altura), (0, 0, 0))
    pixels_saida = imagem_saida.load()
    
    for y in range(altura):
        for x in range(largura):
            rotulo = rotulos[y][x]
            if rotulo > 0:
                if rotulo not in cores:
                    cores[rotulo] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                pixels_saida[x, y] = cores[rotulo]
                
    imagem_saida.save(caminho_saida)

if __name__ == "__main__":
    rotular_imagem("imagem_teste.png", "resultado.png")
