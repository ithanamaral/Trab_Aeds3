import sys
from matrizAdjacencias import MatrizAdjacencias
import caminhoMinimo

def leitura_dimacs(nomeArquivo):
    with open(nomeArquivo, "r") as arquivo:
        primeira_linha = arquivo.readline().strip().split()
        numVertices = int(primeira_linha[0])
        numArestas = int(primeira_linha[1])

        grafo = MatrizAdjacencias(numVertices)

        for _ in range(numArestas):
            linha = arquivo.readline().strip().split()
            origem = int(linha[0])
            destino = int(linha[1])
            peso = int(linha[2])
            grafo.addAresta(origem, destino, peso)

    return grafo

def imprimir_resultado(nome_alg, caminho, custo, tempo, memoria):
    print(f"Algoritmo de {nome_alg}:")
    if isinstance(custo, str) and (custo == "TEMPO LIMITE" or custo == "MEMORIA EXCEDIDA" or custo == "CICLO NEGATIVO"):
        print(f"Resultado: {custo}")
    else:
        print(f"Caminho mínimo: {caminho}")
        print(f"Custo: {custo}")
        print(f"Tempo execução: {tempo:.3f} s")
        print(f"Memória utilizada: {memoria:.4f} MB")
    print("----------------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python main.py <arquivo_grafo> <vertice_origem> <vertice_destino>")
        sys.exit(1)

    arquivo = sys.argv[1]
    origem = int(sys.argv[2])
    destino = int(sys.argv[3])

    grafo = leitura_dimacs(arquivo)

    print("Processando ...\n")
    print("----------------------------------------------------------")

    #dijkstra
    caminho, custo, tempo, memoria = caminhoMinimo.dijkstra(grafo, origem, destino)
    imprimir_resultado("Dijkstra", caminho, custo, tempo, memoria)

    #bellman-Ford
    caminho, custo, tempo, memoria = caminhoMinimo.bellman_ford(grafo, origem, destino)
    imprimir_resultado("Bellman-Ford", caminho, custo, tempo, memoria)

    #floyd-Warshall
    caminho, custo, tempo, memoria = caminhoMinimo.floyd_warshall(grafo, origem, destino)
    imprimir_resultado("Floyd-Warshall", caminho, custo, tempo, memoria)
