from model.fermata import Fermata
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


'''mi aspetto che queste due ridiano gli stessi nodi mA in ordine diverso'''
print("------------------------------------------")
source = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
print (len(nodiBFS))
for i in range(0,10):
    print(nodiBFS[i])
print("------------------------------------------")
nodiDFS = model.getDFSNodesFromEdges(source)
print (len(nodiDFS))
for i in range(0,10):
    print(nodiDFS[i])