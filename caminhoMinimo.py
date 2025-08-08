import time
import math
# import psutil
# import os
import heapq

LIMITE_TEMPO = 600
# MEMORIA_DISPONIVEL_MB = psutil.virtual_memory().available / (1024*1024)


# ---------- DIJKSTRA --------------

def dijkstra(g, s, t):
    inicio_tempo = time.time() # começa o timer pra medir o tempo de execução

    # inicio_mem = psutil.Process(os.getpid()).memory_info().rss

    dist = [math.inf] * g.numVertices  # inicializa as distancias como infinito
    prev = [None] * g.numVertices  # inicializa todos os predecessores como nulo

    dist[s] = 0  # a distância da origem para ela mesma eh zero
    prev[s] = s  # o predecessor da origem eh ela mesma
    O = set(range(g.numVertices)) # conjunto de vertices ainda não processados
    C = set() # conjunto de vertices já processados

    while C != set(range(g.numVertices)):
        # Controle de tempo limite
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"
        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        u = min(O, key=lambda x: dist[x])  #seleciona o vértice com a menor distância
        C.add(u)  #percorre todos os vizinhos de u com seus respectivos pesos
        O.remove(u) #verifica se encontrou caminho mais curto para v

        for v, peso in g.vizinhos(u):
            if v not in C and dist[v] > dist[u] + peso:
                dist[v] = dist[u] + peso # atualiza a distância para v
                prev[v] = u # atualiza o predecessor de v

    caminho = reconstruir_caminho(prev, s, t)

    fim_tempo = time.time()

    # fim_mem = psutil.Process(os.getpid()).memory_info().rss

    return caminho, dist[t], fim_tempo - inicio_tempo, 0.0


#----------- BELLMAN-FORD -------------

def bellman_ford(g, s, t):
    inicio_tempo = time.time()
    # inicio_mem = psutil.Process(os.getpid()).memory_info().rss

    dist = [math.inf] * g.numVertices #inicializa distâncias com infinito
    prev = [None] * g.numVertices #inicializa predecessores com null/ none

    dist[s] = 0
    prev[s] = s

    for _ in range(g.numVertices - 1): # vai repetir |V|-1 vezes
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"

        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        atualizou = False #flag pra verificar se houve atualização

        for u in range(g.numVertices): # percorre todos os vertices
            for v, peso in g.vizinhos(u): #percorre todas as arestas saindo de u
                if dist[u] + peso < dist[v]: # encontrou caminho mais curto para v
                    dist[v] = dist[u] + peso # atualiza a distância
                    prev[v] = u # atualiza o predecessor
                    atualizou = True
        if not atualizou: # se nenhuma distância foi atualizada ele encerra
            break

    #verifica se existe ciclo de peso negativo no grafo
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
    dist = [[math.inf] * V for _ in range(V)] #matriz de distancias inicializada com infinito
    prev = [[None] * V for _ in range(V)] #matriz de predeceessores

    for i in range(V):
        for j in range(V):
            #inicializa distâncias diretas entre os vértices
            if i == j:
                dist[i][j] = 0 #distância de um vértice pra ele mesmo eh zero
                prev[i][j] = i
            elif g.possuiAresta(i, j):
                peso = g.matriz[i][j] if hasattr(g, 'matriz') else dict(g.vizinhos(i))[j]
                dist[i][j] = peso # distância inicial é o peso da aresta
                prev[i][j] = i
            else:
                dist[i][j] = math.inf
                prev[i][j] = None

    for k in range(V):
        if time.time() - inicio_tempo > LIMITE_TEMPO:
            return [], "TEMPO LIMITE", "TEMPO LIMITE", "TEMPO LIMITE"
        # if uso_memoria_mb() > MEMORIA_DISPONIVEL_MB:
        #     return [], "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA", "MEMORIA EXCEDIDA"

        #verifica se passar por k deixa o caminho entre i e j mais curto
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
# Funções auxiliares
#---------------------

# def uso_memoria_mb():
#     return psutil.Process(os.getpid()).memory_info().rss / (1024*1024)

#reconstroi o caminho usando a lista de predecessores de s até t
def reconstruir_caminho(prev, s, t):
    caminho = [] # lista que vai guardar o caminho na ordem certa
    u = t # começa do destino
    if prev[u] is None:
        return []
    while u != s: #volta até chegar na origem
        caminho.insert(0, u)  # insere o vértice no inicio da lista
        u = prev[u] # vai para o predecessor
        if u is None: # se chegar em vértice sem predecessor, entao não existe caminho
            return []
    caminho.insert(0, s) #insere a origem no início
    return caminho

#reconstroi o caminho para floyd-warshall usando a matriz de predecessores
def reconstruir_caminho_fw(prev, s, t):
    if prev[s][t] is None: #não tem predecessor = não tem caminho
        return []
    caminho = [t] #começa com o destino
    while t != s: #volta até a origem
        t = prev[s][t] #pega o vertice anterior no caminho
        caminho.insert(0, t) #coloca no inicio da lista
    return caminho
