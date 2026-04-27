from model.model import Model

model = Model()
#verifico che il grafo sia vuoto
print("Numero nodi: ", model.get_numnodi())
print("Numero archi: ", model.get_numarchi())

model.buildGraph()
#per esempio stampo un numero di nodi
print("Numero nodi: ", model.get_numnodi())
#avrò anche archi
print("Numero archi: ", model.get_numarchi())