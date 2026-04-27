from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() #istanzio un grafo semplice e orientato

    def buildGraph(self):
        #voglio popolae il grafo con la lista di oggetti (fermate)
        #è bene assicurarsi che all'inizio il grafo sia vuoto altrimenti aggiungo nodi a uno esistente
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        #per verifiacares se l'ho costruito bene creo "testModel"
        self.addedges()

    def addedges(self ):
        #devo verificare se due fermate hanno un collegamento.
        for u in self._fermate:
            for v in self._fermate: #questo doppio ciclo for è un po troppo lungo e fa perdere tempo
                if DAO.hasconn(u, v): #SE ritorna true:
                    self._grafo.add_edge(u, v) #posso aggiungere al grafo la coppia di nodi

    #siccome quesTO addedges è lento penso a un altra soluzione
    def addedges2(self):


    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate