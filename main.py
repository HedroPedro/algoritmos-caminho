from sys import maxsize
from random import randint
import time

def main():
    graph = {'A': {'B':randint(1, 10), 'C':randint(1, 10), 'D':randint(1, 10)},
             'B': {'C':randint(1, 10), 'D':randint(1, 10)},
             'C': {'D':randint(1, 10)},
             'D': {'B':randint(1, 10), 'C':randint(1, 10), 'E':randint(1, 10)},
             'E': {'D': 15}
            }
    posicao = {
        'A': (0, 0),
        'B': (1, 0),
        'C': (0, 1),
        'D': (1, 1),
        'E': (2, 2)
    }
    print(graph)
    print(computar_dijkstra(graph, 'A', 'E'))
    print(computar_a_estrela(graph, 'A', 'E', posicao))

def constroi_caminho(visitados, fim):
    caminho = []
    atual = fim
    while atual != None:
        caminho.append(atual)
        atual = visitados[atual]
    caminho.reverse()
    return caminho

def computar_dijkstra(grafo, inicio, fim):
    distancias = {vertice : maxsize for vertice in grafo}
    visitados = {vertice : None for vertice in grafo}
    vertices_fechados = set()
    distancias[inicio] = 0
    while vertices_fechados != set(grafo):
        vertice_min = None
        distancia_min = maxsize
        for vertice in grafo:
            if vertice not in vertices_fechados and distancias[vertice] < distancia_min:
                vertice_min = vertice
                distancia_min = distancias[vertice]

        if vertice_min == None:
            break

        vertices_fechados.add(vertice_min)
        if vertice_min == fim:
            return constroi_caminho(visitados, fim), distancias[fim]
        
        for vizinho, peso in grafo[vertice_min].items():
            if distancias[vertice_min] + peso < distancias[vizinho]:
                distancias[vizinho] = distancias[vertice_min] + peso
                visitados[vizinho] = vertice_min

    return [], float("inf")

def heuristica(atual, final):
    return (abs(atual[0]-final[0])**2 + abs(atual[1]-final[1])**2)**0.5

def computar_a_estrela(grafo : dict[dict[str : int]], inicio : str, fim : str, posicoes : dict[tuple]):
    lista_aberta = set(inicio)
    lista_fechada = set()
    dist_g = {vertice : maxsize for vertice in grafo} #Distancia real
    dist_f = {vertice : maxsize for vertice in grafo} #Distancia presumida
    visitados = {vertice : None for vertice in grafo} #Vertices visitados
    dist_g[inicio] = 0
    dist_f[inicio] = heuristica(posicoes[inicio], posicoes[fim])

    while lista_aberta:
        vertice_min = ''
        dist_min = maxsize

        for vertice in grafo:
            if dist_min > dist_f[vertice] and vertice not in lista_fechada:
                vertice_min = vertice
                dist_min = dist_f[vertice]

        if vertice_min == '':
            break
        if vertice_min == fim:
            return constroi_caminho(visitados, fim), int(dist_f[fim])
        lista_aberta.remove(vertice_min)

        for vizinho, peso in grafo[vertice_min].items():
            tentativa_dist_g = dist_g[vertice_min] + peso
            if tentativa_dist_g < dist_g[vizinho]:
                dist_g[vizinho] = tentativa_dist_g
                dist_f[vizinho] = dist_g[vizinho] + heuristica(posicoes[vizinho], posicoes[fim])
                visitados[vizinho] = vertice_min
            if vizinho not in lista_aberta:
                lista_aberta.add(vizinho)

        lista_fechada.add(vertice_min)
    return [], float("inf")

if __name__ == "__main__":
    main()