# Funções auxiliares para detectar ganhos

def flip_horizontal(result):
    # Inverte os resultados horizontalmente para mantê-los em uma lista mais legível
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    # 'Rotaciona' 90 graus para obter a representação em texto da rotação na ordem correta
    linhas, colunas = len(horizontal_values), len(horizontal_values[0])
    matriz_rotacionada = [[""] * linhas for _ in range(colunas)]
    for x in range(linhas):
        for y in range(colunas):
            matriz_rotacionada[y][linhas - x - 1] = horizontal_values[x][y]
    # Inverte cada linha para alinhar da maneira esperada
    return [linha[::-1] for linha in matriz_rotacionada]

def longest_seq(hit):
    # Calcula a subsequência mais longa de índices consecutivos
    comprimento_atual = 1
    comprimento_max = 1
    inicio, fim = 0, 0
    for i in range(len(hit) - 1):
        # Verifica se os índices são sequenciais
        if hit[i] == hit[i + 1] - 1:
            comprimento_atual += 1
            if comprimento_atual > comprimento_max:
                comprimento_max = comprimento_atual
                inicio = i + 2 - comprimento_atual
                fim = i + 2
        else:
            comprimento_atual = 1
    # Retorna a subsequência mais longa encontrada
    return hit[inicio:fim]
