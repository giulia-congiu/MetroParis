from model.fermata import Fermata
from model.model import Model

model = Model()
#verifico che il grafo sia vuoto
print("Numero nodi: ", model.get_numnodi())
print("Numero archi: ", model.get_numarchi())

#model.buildGraph()
model.buildGraphPesato()
#per esempio stampo un numero di nodi
print("Numero nodi: ", model.get_numnodi())
#avrò anche archi
print("Numero archi: ", model.get_numarchi())
#il numero di archi che sto aggiungendo è 1428
#facendolo da dbeaver il numero di connessioni sarà
'''avviene perchè ci sono alcune fermate che sono servite da più linee ovvero ci saranno casi
in cui ho stesso u e stesso v ma saranno due collegamenti diversi. Per come ho scritto il codice però questo
non viene concepito e quando c'è un 'doppio' non viene aggiunto al grafico.
Sarebbe diverso creando un MULTIGRAFO. Per gestire questa cosa ho due opzioni:
1- il grafo è un grafo pesato, in cui il peso rappresenta il numero di “Linee” che
connettono le due “Fermate” --- FACCIAMO QUESTA ORA
2- il grafo è un multi-grafo, in cui se esistono più “Linee” che collegano due
“Fermate”, allora saranno aggiunti altrettanti archi.'''


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

print("===========================================")

print("Archi con peso 2")
archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0], "->", a[1], ":", a[2]["weight"])