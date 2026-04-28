from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() #istanzio un grafo semplice e orientato
        '''mi serve passare dalla connessione alla fermata:
        creo un dizionario che posso interrogare con la chiave di uno dei valori di connessione (idArrivo in questo caso)
        e mi ritorna il valore corrispondente dell'altra dataclass, la fermata
        (in questo caso posso farlo nell'init ma non sempre)'''
        self._idMapFermate= {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f
            #dato l'id della fermata, ritorno il tipo fermata corrispondente


    def buildGraph(self):
        #voglio popolae il grafo con la lista di oggetti (fermate)
        #è bene assicurarsi che all'inizio il grafo sia vuoto altrimenti aggiungo nodi a uno esistente
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        #per verifiacares se l'ho costruito bene creo "testModel"
        self.addedges3()

    def addedges(self ):
        #devo verificare se due fermate hanno un collegamento.
        for u in self._fermate:
            for v in self._fermate: #questo doppio ciclo for è un po troppo lungo e fa perdere tempo
                if DAO.hasconn(u, v): #SE ritorna true:
                    self._grafo.add_edge(u, v) #posso aggiungere al grafo la coppia di nodi

    #siccome quesTO addedges è lento penso a un altra soluzione
    def addedges2(self):
        for u in self._fermate:
            for connessione in DAO.getvicini(u): #voglio l'elenco dei vicini del nodo
                v= self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)
                
    '''posso fare ancora meglio di addages2: posso pensare a un modo di costruire
    gli edge senza fare un ciclo for, ma solo leggendo la tabella connessioni: due nodi sono collegati
    solo se c'è una connessione tra loro, se leggo tutte le connessioni che ho nel dao ho fatto'''

    def addedges3(self): #funzione che mi tira fuori tutti gli edge
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate