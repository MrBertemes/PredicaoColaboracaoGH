import json, os

def generate_cypher(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    queries = []

    for user, dados in data.items():
        ativ = dados.get("atividade", "")
        repos = dados.get("repositorios", {})
        queries.append(f"CREATE (:User {{name: \"{user}\", atividade: \"{ativ}\"}});")
        for repo, details in repos.items():
            created = details.get("created", "not defined")
            first = details.get("first", "")
            last = details.get("last", "")

            queries.append(f"CREATE (:Repository {{name: \"{repo}\", first: \"{first}\", create: \"{created}\", last: \"{last}\"}});")

            queries.append(f"MATCH (u:User {{name: \"{user}\"}}), (r:Repository {{name: \"{repo}\"}})\n"
                        f"WITH u, r\n"
                        f"CREATE (u)-[:CONTRIBUTES_TO]->(r);\n")

            collaborators = details.get("colab", [])
            for colabs in collaborators:
                for colab, times in colabs.items():
                    print(colab, times)
                    queries.append(f"MERGE (:User {{name: \"{colab}\"}});")

                    queries.append(f"MATCH (c:User {{name: \"{colab}\"}}), (r:Repository {{name: \"{repo}\"}})\n"
                                f"WITH c, r \n"
                                f"CREATE (c)-[:COLLABORATES_ON {{times: {times}}}]->(r);\n")

    return queries

input_file_path = 'final_3.json'


cypher_queries = generate_cypher(input_file_path)


for query in cypher_queries:
    print(query)
