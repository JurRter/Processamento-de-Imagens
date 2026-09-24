# Comparação dos filtros

As máscaras foram conferidas visualmente na página 4 de `Aula10_Filtragem.pdf`:

```text
a:  0  1  0     b:  1  1  1     c:  0 -1  0     d: -1 -1 -1
    1 -4  1         1 -8  1        -1  4 -1        -1  8 -1
    0  1  0         1  1  1         0 -1  0        -1 -1 -1
```

## Teste numérico reproduzível

Em uma imagem preta 5×5, foi colocado um pixel de intensidade 10 no centro. Os testes em `testes/verificar.py` confirmaram:

| Máscara | Resposta no centro | Resposta em cada vizinho lateral | Resposta em cada vizinho diagonal |
| --- | ---: | ---: | ---: |
| a | -40 | 10 | 0 |
| b | -80 | 10 | 10 |
| c | 40 | -10 | 0 |
| d | 80 | -10 | -10 |

As máscaras b e d incluem as diagonais e têm maior resposta central nesse teste. As máscaras a e c consideram os quatro vizinhos laterais. A máscara c inverte exatamente o sinal de a; d inverte o de b.

Com valores negativos zerados na imagem PNG, a e b mostram os vizinhos positivos em torno do centro; c e d mostram o centro positivo. Por isso trocar o sinal da máscara altera as bordas visíveis após a saturação, mesmo que as respostas brutas sejam opostas. Valores acima de 255 também são limitados, o que pode esconder diferenças de intensidade. Os CSVs preservam essas diferenças para comparação.

Em uma região constante, longe da borda, as quatro respostas são zero: a soma dos coeficientes é zero. O padding de zeros pode criar resposta na borda externa de uma imagem constante, pois introduz uma transição entre a imagem e o exterior.

## Resultado na imagem do repositório

Também foi usada `Segunda Implementação - Rotulação/imagem_teste.png`, com 1152×648 pixels. A inspeção das imagens geradas mostrou os contornos das seis figuras, com respostas mais abrangentes nas máscaras que incluem diagonais. A contagem das respostas numéricas antes da saturação foi:

| Máscara | Menor valor | Maior valor | Pixels positivos | Pixels negativos |
| --- | ---: | ---: | ---: | ---: |
| a | -510 | 765 | 3010 | 2986 |
| b | -1275 | 1275 | 4227 | 4180 |
| c | -765 | 510 | 2986 | 3010 |
| d | -1275 | 1275 | 4180 | 4227 |

A inversão entre a/c e b/d aparece também nas contagens. Com a e b, aparecem os pixels do lado escuro das transições; com c e d, os do lado claro. A imagem binária tem contraste máximo, portanto muitos valores atingem 255 no PNG. As amplitudes dos CSVs tornam a diferença entre quatro e oito vizinhos mais clara. A magnitude de Sobel destacou os contornos nas duas direções e teve máximo bruto de aproximadamente 1140,39, saturado em 255 na visualização.

## Sobel

As páginas 16 e 17 usam as seguintes componentes, seguindo a ordem dos pixels z1 a z9:

```text
gx: -1 -2 -1     gy: -1  0  1
     0  0  0         -2  0  2
     1  2  1         -1  0  1
```

O nome gx segue a convenção do slide: sua máscara mede a variação entre a linha inferior e a superior, realçando bordas horizontais. Gy mede a variação entre as colunas direita e esquerda, realçando bordas verticais. A magnitude é `sqrt(gx² + gy²)`, conforme a página 14.

No centro de uma rampa com linhas `[0, 10, 20]`, o teste obteve gx = 0, gy = 80 e magnitude = 80. Com a rampa na outra direção, obteve gx = 80 e gy = 0. Em uma rampa decrescente nas duas direções, obteve gx = gy = -80 e magnitude aproximadamente 113,14. Isso confirma que a magnitude usa os sinais originais, antes da conversão para PNG.

As imagens PNG das componentes zeram valores negativos, conforme a opção escolhida no enunciado. Consulte os CSVs para observar as componentes negativas. Na magnitude, tanto as transições claras para escuras quanto as escuras para claras podem aparecer.

## Repetir com uma imagem

Na raiz do repositório:

```powershell
python "Sétima Implementação - Laplaciano e Sobel/filtros.py"
```

Informe `Segunda Implementação - Rotulação/imagem_teste.png` quando solicitado. Compare `laplaciano_a.png` a `laplaciano_d.png` na pasta de execução, junto de `sobel_gx.png`, `sobel_gy.png` e `sobel_magnitude.png`. Todos mantêm as dimensões da entrada. As medições acima também podem ser reproduzidas executando em uma pasta separada e informando o caminho absoluto da entrada.
