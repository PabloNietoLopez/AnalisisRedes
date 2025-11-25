def inicializar(edges_list, nombre_red):
    diccionario = crea_diccionario(edges_list)
    diccionario_grados = crea_diccionario_grado_nodos(diccionario)
    diccionario_clustering = crea_diccionario_clustering(diccionario)
    diccionario_resul = {}
    diccionario_resul["nombre_red"] = nombre_red
    return diccionario, diccionario_grados, diccionario_clustering, diccionario_resul


def crea_diccionario(edges):
    diccionario_ady = {}
    for u, v in edges:
        if u not in diccionario_ady:
            diccionario_ady[u] = []
        if v not in diccionario_ady:
            diccionario_ady[v] = []
        # grafo no dirigido
        diccionario_ady[u].append(v)
        diccionario_ady[v].append(u)
    return diccionario_ady


def crea_diccionario_grado_nodos(diccionario_ady):
    dicc_grado = {}
    for u, adys in list(diccionario_ady.items())[:100]:
        dicc_grado[u] = len(adys)
    return dicc_grado


def crea_diccionario_clustering(diccionario):
    diccionario_clust = {}
    for u, adys in list(diccionario.items())[:100]:
        grado = len(adys)
        if grado < 2:
            coeficiente_clustering = 0
        else:
            aristas_entre_vecinos = 0
            for vecino1 in adys:
                for vecino2 in adys:
                    if vecino1 != vecino2:
                        if vecino2 in diccionario[vecino1]:
                            aristas_entre_vecinos += 1
            coeficiente_clustering = (2 * aristas_entre_vecinos) / (grado * (grado - 1))
        diccionario_clust[u] = [coeficiente_clustering]
    return diccionario_clust
