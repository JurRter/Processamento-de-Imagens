def ampliar_reduzir_vizinho(matriz_imagem, nova_altura, nova_largura):
    altura_original = len(matriz_imagem)
    largura_original = len(matriz_imagem[0])
    
    nova_matriz = []
    
    for linha in range(nova_altura):
        nova_linha = []
        for coluna in range(nova_largura):
            pos_x_original = int(linha * (altura_original / nova_altura))
            pos_y_original = int(coluna * (largura_original / nova_largura))
            
            nova_linha.append(matriz_imagem[pos_x_original][pos_y_original])
            
        nova_matriz.append(nova_linha)
        
    return nova_matriz


def ampliar_reduzir_bilinear(matriz_imagem, nova_altura, nova_largura):
    altura_original = len(matriz_imagem)
    largura_original = len(matriz_imagem[0])
    
    nova_matriz = []
    
    for linha in range(nova_altura):
        nova_linha = []
        for coluna in range(nova_largura):
            
            if nova_altura > 1:
                x = (linha * (altura_original - 1)) / (nova_altura - 1)
            else:
                x = 0
                
            if nova_largura > 1:
                y = (coluna * (largura_original - 1)) / (nova_largura - 1)
            else:
                y = 0
                
            x_inferior = int(x)
            y_inferior = int(y)
            
            x_superior = x_inferior + 1
            if x_superior >= altura_original:
                x_superior = altura_original - 1
                
            y_superior = y_inferior + 1
            if y_superior >= largura_original:
                y_superior = largura_original - 1
                
            pixel_topo_esq = matriz_imagem[x_inferior][y_inferior]
            pixel_topo_dir = matriz_imagem[x_inferior][y_superior]
            pixel_baixo_esq = matriz_imagem[x_superior][y_inferior]
            pixel_baixo_dir = matriz_imagem[x_superior][y_superior]
            
            pixel_final = (
                pixel_topo_esq
                + pixel_topo_dir
                + pixel_baixo_esq
                + pixel_baixo_dir
            ) / 4
            
            nova_linha.append(int(pixel_final))
            
        nova_matriz.append(nova_linha)
        
    return nova_matriz

# Teste básico para mostrar que funciona na aula
imagem_teste = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

print("Teste de Redução (Vizinho):")
for l in ampliar_reduzir_vizinho(imagem_teste, 5, 5):
    print(l)

print("\nTeste de Ampliação (Bilinear):")
for l in ampliar_reduzir_bilinear(imagem_teste, 2, 2):
    print(l)