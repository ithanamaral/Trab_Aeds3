import time
import math
# import psutil
# import os
import heapq

LIMITE_TEMPO = 600
# MEMORIA_DISPONIVEL_MB = psutil.virtual_memory().available / (1024*1024)


# ---------- DIJKSTRA --------------

def dijkstra(g, s, t):
    inicio_tempo = time.time()
    # inicio_mem = psutil.Process(os.getpid()).memory_info().rss

    dist = [math.inf] * g.numVertices
    prev = [None] * g.numVertices

    dist[s] = 0
    prev[s] = s
    O = set(range(g.numVertices))
    C = set()

    while C != set(range(g.numVertices)):
        # Controle de tempo limite
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"
        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        u = min(O, key=lambda x: dist[x])
        C.add(u)
        O.remove(u)

        for v, peso in g.vizinhos(u):
            if v not in C and dist[v] > dist[u] + peso:
                dist[v] = dist[u] + peso
                prev[v] = u

    caminho = reconstruir_caminho(prev, s, t)

    fim_tempo = time.time()
    # fim_mem = psutil.Process(os.getpid()).memory_info().rss
    return caminho, dist[t], fim_tempo - inicio_tempo, 0.0


# ---------- BELLMAN-FORD --------------

def bellman_ford(g, s, t):
    inicio_tempo = time.time()
    # inicio_mem = psutil.Process(os.getpid()).memory_info().rss

    dist = [math.inf] * g.numVertices
    prev = [None] * g.numVertices

    dist[s] = 0
    prev[s] = s

    for _ in range(g.numVertices - 1):
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"
        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        atualizou = False
        for u in range(g.numVertices):
            for v, peso in g.vizinhos(u):
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    atualizou = True
        if not atualizou:
            break

    for u in range(g.numVertices):
        for v, peso in g.vizinhos(u):
            if dist[u] + peso < dist[v]:
                return [], "CICLO NEGATIVO", "CICLO NEGATIVO", "CICLO NEGATIVO"

    caminho = reconstruir_caminho(prev, s, t)

    fim_tempo = time.time()
    # fim_mem = psutil.Process(os.getpid()).memory_info().rss
    return caminho, dist[t], fim_tempo - inicio_tempo, 0.0



#----------- FLOYD-WARSHALL ---------------

def floyd_warshall(g, s, t):
    inicio_tempo = time.time()
    # inicio_mem = psutil.Process(os.getpid()).memory_info().rss

    V = g.numVertices
    dist = [[math.inf] * V for _ in range(V)]
    prev = [[None] * V for _ in range(V)]

    for i in range(V):
        for j in range(V):
            if i == j:
                dist[i][j] = 0
                prev[i][j] = i
            elif g.possuiAresta(i, j):
                peso = g.matriz[i][j] if hasattr(g, 'matriz') else dict(g.vizinhos(i))[j]
                dist[i][j] = peso
                prev[i][j] = i
            else:
                dist[i][j] = math.inf
                prev[i][j] = None

    for k in range(V):
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"
        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        for i in range(V):
            for j in range(V):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]

    caminho = reconstruir_caminho_fw(prev, s, t)

    fim_tempo = time.time()
    # fim_mem = psutil.Process(os.getpid()).memory_info().rss
    return caminho, dist[s][t], fim_tempo - inicio_tempo, 0.0


#---------------------
# funções auxiliares
#---------------------

# def uso_memoria_mb():
#     return psutil.Process(os.getpid()).memory_info().rss / (1024*1024)

def reconstruir_caminho(prev, s, t):
    caminho = []
    u = t
    if prev[u] is None:
        return []
    while u != s:
        caminho.insert(0, u)
        u = prev[u]
        if u is None:
            return []
    caminho.insert(0, s)
    return caminho

def reconstruir_caminho_fw(prev, s, t):
    if prev[s][t] is None:
        return []
    caminho = [t]
    while t != s:
        t = prev[s][t]
        caminho.insert(0, t)
    return caminho
