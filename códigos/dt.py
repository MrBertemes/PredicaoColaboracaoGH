import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

# Carregar o grafo
G = nx.read_gexf("grafoFinal.gexf")

# Lista de nós que representam "egressos" no grafo
egressos = [n for n in G.nodes() if G.nodes[n].get("tipo") == "egresso"]

def generate_features(egresso, v):
    # Número de vizinhos em comum
    common_neigh = len(list(nx.common_neighbors(G, egresso, v)))
    return [common_neigh]

# Lista para armazenar os resultados
resultados = []

# Função para realizar a predição de arestas para um "egresso"
def predict_for_egresso(egresso):
    # Gerar arestas existentes e não existentes envolvendo o "egresso"
    edges = [(egresso, v) for v in G.neighbors(egresso)]
    non_edges = [(egresso, v) for v in G.nodes() if v != egresso and not G.has_edge(egresso, v)]
    
    # Gerar as features para as arestas existentes
    X_edges = np.array([generate_features(egresso, v) for _, v in edges]).reshape(-1, 6)
    y_edges = np.ones(len(edges))  # 1 para indicar que a aresta existe
    
    # Gerar as features para as não arestas
    X_non_edges = np.array([generate_features(egresso, v) for _, v in non_edges]).reshape(-1, 6)
    y_non_edges = np.zeros(len(non_edges))  # 0 para indicar que a aresta não existe
    
    # Combinar os dados
    X = np.concatenate([X_edges, X_non_edges])
    y = np.concatenate([y_edges, y_non_edges])
    
    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Treinar o modelo de árvore de decisão com parâmetros ajustados
    clf = DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_split=4)
    clf.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = clf.predict(X_test)
    
    # Avaliar o desempenho
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Armazenar os resultados em um dicionário
    resultados.append({
        "egresso": egresso,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "conf_matrix": conf_matrix
    })

# Aplicar para cada "egresso"
for egresso in egressos:
    predict_for_egresso(egresso)

# Imprimir os resultados
print("\nResultados para cada egresso:\n")
for resultado in resultados:
    print(f"Egresso: {resultado['egresso']}")
    print(f"Acurácia: {resultado['accuracy']:.2f}")
    print(f"Precisão: {resultado['precision']:.2f}")
    print(f"Revocação: {resultado['recall']:.2f}")
    print(f"F1-score: {resultado['f1_score']:.2f}")
    print("Matriz de Confusão:")
    print(resultado["conf_matrix"])
    print("-" * 40)
