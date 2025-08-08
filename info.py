import listaAdjacencias
import matrizAdjacencias

# retorna a densidade do grafo:
def densidade(grafo):
    maxArestas = grafo.numVertices * (grafo.numVertices - 1)
    return float(grafo.numArestas) / float(maxArestas)

# retorna o complemento do grafo:
def complemento(grafo):
    comp = listaAdjacencias.ListaAdjacencias(grafo.numVertices)

    for v1 in range(grafo.numVertices):
        for v2 in range(grafo.numVertices):
            if (not grafo.possuiAresta(v1, v2)) and v1 != v2:
                comp.addAresta(v1, v2)
    return comp

# retorna True se o grafo eh completo:
def completo(grafo):
    print("Metodo completo(grafo) nao foi implementado ainda!\n")
    return None

# retorna True se o grafo eh regular:
def regular(grafo):
    print("Metodo regular(grafo) nao foi implementado ainda!\n")
    return None


# retorna um subgrafo induzido pelo conjunto de vertices:
def subgrafo(grafo, vertices):
    print("Metodo subgrafo(grafo, vertices) nao foi implementado ainda!\n")
    return None
