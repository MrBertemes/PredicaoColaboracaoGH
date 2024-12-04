import networkx as nx
import numpy as np

# Crie seu grafo
G = nx.read_gexf("grafoFinal.gexf")

# Função para realizar o teste de pequeno mundo
def small_world_test(G, niter=100, nrand=10):
    if not nx.is_connected(G):
        # Se o grafo não for conexo, use o maior componente conexo
        largest_cc = max(nx.connected_components(G), key=len)
        G_largest_cc = G.subgraph(largest_cc)
    else:
        G_largest_cc = G

    
    # Calcular as métricas do grafo original
    L = nx.average_shortest_path_length(G_largest_cc)
    C = nx.average_clustering(G_largest_cc)
    
    # Calcular as métricas para grafos aleatórios
    L_rand = []
    C_rand = []
    for _ in range(nrand):
        R = nx.gnm_random_graph(G.number_of_nodes(), G.number_of_edges())
        if nx.is_connected(R):
            L_rand.append(nx.average_shortest_path_length(R))
            C_rand.append(nx.average_clustering(R))
        else:
            # Se o grafo aleatório não for conexo, considerar o maior componente conexo
            largest_cc = max(nx.connected_components(R), key=len)
            R_largest_cc = R.subgraph(largest_cc)
            L_rand.append(nx.average_shortest_path_length(R_largest_cc))
            C_rand.append(nx.average_clustering(R_largest_cc))
    
    L_rand_mean = np.mean(L_rand)
    C_rand_mean = np.mean(C_rand)
    
    # Comparar com o grafo aleatório
    small_world_coefficient = (C / C_rand_mean) / (L / L_rand_mean)
    print(f"({C} /{ C_rand_mean}) / ({L} / {L_rand_mean})")
    
    return {
        "L": L,
        "C": C,
        "L_rand_mean": L_rand_mean,
        "C_rand_mean": C_rand_mean,
        "small_world_coefficient": small_world_coefficient,
        "is_small_world": small_world_coefficient > 1
    }

# Realizar o teste de pequeno mundo
result = small_world_test(G)

# Mostrar os resultados
print("Comprimento Médio do Caminho (G):", result["L"])
print("Coeficiente de Aglomeração Médio (G):", result["C"])
print("Comprimento Médio do Caminho (Grafo Aleatório):", result["L_rand_mean"])
print("Coeficiente de Aglomeração Médio (Grafo Aleatório):", result["C_rand_mean"])
print("Coeficiente de Pequeno Mundo:", result["small_world_coefficient"])
print("É um grafo de pequeno mundo?", result["is_small_world"])