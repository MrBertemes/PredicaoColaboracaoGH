import json
import networkx as nx
import random

def random_edge(graph, n, egresso):
    edges = list(graph.edges(egresso))
    removed_edges = []
    for i in range(n):
        chosen_edge = random.choice(edges)
        if (egresso, chosen_edge[1]) in edges and (egresso, chosen_edge[1]) not in removed_edges:
            graph.remove_edge(egresso, chosen_edge[1])
            removed_edges.append((egresso, chosen_edge[1]))

    return graph, removed_edges

def consenso_lp(G, no, threshold=1.5):
    arg = G, [(no, n) for n in G.nodes if n != no and not G.has_edge(no, n)]

    pred_jaccard = list(nx.link_prediction.jaccard_coefficient(arg[0], arg[1]))
    pred_adamic_adar = list(nx.link_prediction.adamic_adar_index(arg[0], arg[1]))

    arestas_notas = {}

    def att_notas(predictions):
        for u, v, p in predictions:
            if (u, v) not in arestas_notas and (v, u) not in arestas_notas:
                arestas_notas[(u, v)] = p
            else:
                if (u, v) in arestas_notas:
                    arestas_notas[(u, v)] += p
                else:
                    arestas_notas[(v, u)] += p
    
    pred_jaccard = sorted([(u, v, score) for (u,v,score) in pred_jaccard ], key=lambda x: x[2], reverse=True)
    maior_jaccard = pred_jaccard[0][2]
    pred_jaccard = sorted([(u, v, score/(maior_jaccard if maior_jaccard != 0 else 1)) for (u,v,score) in pred_jaccard], key=lambda x: x[2], reverse=True)


    pred_adamic_adar = sorted([(u, v, score) for (u,v,score) in pred_adamic_adar ], key=lambda x: x[2], reverse=True)
    maior_adamic_adar = pred_adamic_adar[0][2]
    pred_adamic_adar = sorted([(u, v, score/(maior_adamic_adar if maior_adamic_adar != 0 else 1)) for (u,v,score) in pred_adamic_adar], key=lambda x: x[2], reverse=True)


    # Update scores with the predictions
    att_notas(pred_jaccard)
    att_notas(pred_adamic_adar)
    consenso_arestas = sorted([(u, v, score) for (u, v), score in arestas_notas.items() if score >= threshold], key=lambda x: x[2], reverse=True)

    return consenso_arestas

def pred(egresso):
    G_teste = nx.read_gexf("grafoFinal.gexf") # real
    qtdArestas = len(G_teste.edges(egresso))
    if qtdArestas == 0:
        return (0, 0, 0)
    min = int((qtdArestas/10)) if (qtdArestas/10) > 1 else 1
    max = int((qtdArestas/2)) if (qtdArestas/2) > 1 else 1
    rand = random.randint(min, max)

    G_pred = nx.read_gexf("grafoFinal.gexf") # pred
    G_pred,removed_edges  = random_edge(G_pred, rand, egresso)

    pred = consenso_lp(G_pred, egresso, 1.5)
    pred = sorted(pred, key=lambda x:x[2], reverse=True)

    vp = 0
    vn = 0
    fp = 0
    fn = 0

    for i in pred[:len(removed_edges)]:
        if (i[0], i[1]) in removed_edges:
            vp += 1
        else:
            fp += 1

    for i in removed_edges:
        if i not in [(u,v) for (u,v,p) in pred]:
            fn +=1

    precisao = vp / (vp+fp) if (vp+fp) != 0 else 1
    recall = vp / (vp+fn) if (vp+fn) != 0 else 1
    f1 = (precisao*recall)/(precisao+recall) if (precisao+recall) != 0 else 1
    eficacia = (vp+vn)/(vp+vn+fn+fp) if (vp+vn+fn+fp) != 0 else 1
    return (precisao, recall, f1, eficacia)

f = open('dados.json','r') 
dados = json.load(f)
resultado = {}
for user, colabs in dados.items():
    resultado[user] = ()
    aux = 0
    precisao = 0
    recall = 0
    f1 = 0
    eficacia = 0

    for i in range(30):
        p,r, ff,e = pred(user)
        precisao += p
        recall += r
        f1 += ff
        eficacia += e
        aux += 1

    precisao = precisao/len
    recall = recall/len
    f1 = f1/len
    eficacia = eficacia/len
    resultado[user] = (precisao, recall, f1, eficacia)

json_obj = json.dumps(resultado, indent= 4)

j = open("avaliacao.json","+w")
j.write(json_obj)
j.close()

