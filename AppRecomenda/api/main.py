from typing import Union
import networkx as nx
import random
import linkpred
from fastapi import FastAPI
from grafo import grafo, info

app = FastAPI()

def combina_lp(G, no, threshold=1.5):
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

    # print(f"Maior jaccard: {pred_jaccard[0][2]}\n{pred_jaccard[:10]}")
    # print(f"Maior jaccard: {pred_adamic_adar[0][2]}\n{pred_adamic_adar[:10]}")

    # Update scores with the predictions
    att_notas(pred_jaccard)
    att_notas(pred_adamic_adar)
    consenso_arestas = sorted([(u, v, score) for (u, v), score in arestas_notas.items() if score >= threshold], key=lambda x: x[2], reverse=True)

    return consenso_arestas



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pred/{nome_egresso}")
def predicao(nome_egresso: str):
    G = nx.read_gexf("grafoFinal.gexf")
    edges_to_add = combina_lp(G, nome_egresso)
    print(sorted(edges_to_add, key=lambda x: x[2], reverse=True))
    return {"pred":edges_to_add};



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}