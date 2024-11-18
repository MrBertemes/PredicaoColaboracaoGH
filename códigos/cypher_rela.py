import json, os

def generate_cypher(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    queries = []

    for user, colabs in data.items():
        queries.append(f"CREATE (:User {{name: \"{user}\"}});")
        for colab, times in colabs.items():
            queries.append(f"CREATE (:User {{name: \"{colab}\"}});")
            queries.append(f"MATCH (u:User {{name: \"{user}\"}}), (c:User {{name: \"{colab}\"}})\n"
                           f"WITH u, c\n"
                           f"CREATE (c)-[:RELATED {{times: {times}}}]-(u);\n")
    
    return queries

def cypherToFile(queries):
    for query in queries:
        os.system(f"echo '{query}' >> teste.txt")

input_file_path = 'relacoes.json'

cypher_queries = generate_cypher(input_file_path)

