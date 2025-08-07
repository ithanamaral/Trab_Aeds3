import sys


def floyd_warshall(num_vertices, arestas):
    """Calcula as distâncias mais curtas entre todos os pares de cidades."""
    # Prepara a "Tabela de Tempos" (dist) e a "Tabela de Placas" (prev)
    contagem_inicial = time.time()
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    prev = [[None] * num_vertices for _ in range(num_vertices)]

    for i in range(num_vertices):
        dist[i][i] = 0
        prev[i][i] = i

    for (u, v), peso in arestas.items():
        dist[u][v] = peso
        prev[u][v] = u

    # Testa cada cidade 'k' como uma possível "ponte" para um atalho
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]
    
    contagem_final = time.time()  # Fim do time
    tempo_execucao = contagem_final - contagem_inicial
    return dist, prev, tempo_execucao
