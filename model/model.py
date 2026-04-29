from database.DAO import DAO
import networkx as nx
from datetime import datetime

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #leggo tutte le fermate dal DAO
        self._grafo = nx.DiGraph() #istanzio un grafo semplice e orientato
        '''Creo un idMap perchè mi serve passare dalla connessione alla fermata:
        creo un dizionario che posso interrogare con la chiave di uno dei valori di connessione (idArrivo in questo caso)
        e mi ritorna il valore corrispondente dell'altra dataclass, la fermata
        (in questo caso posso farlo nell'init ma non sempre)'''
        self._idMapFermate= {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f
            #dato l'id della fermata (chiave primaria della dataclasss (uso quasi sempre quellA)),
            # ritorno l'oggetto fermata corrispondente

    '''4 ESPLORAZIONI DEL GRAFO UGUALI A COPPIE, CAMBIA SOLO IL MODO IN CUI MI VIENE RIDATO L'OUTPUT
    IN UN CASO VIENE RESTITUITO a RAPPR A ARCHI IN UNO A RAPPR AD ALBERO'''

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source) #iterable di tuple
        nodiBFS = []
        for u, v in archi: #u è il nodo da cui parto (l'ho già visto)
            nodiBFS.append(v)
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi #dovrei escludere il nodo source

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)  # iterable di tuple
        nodiDFS = []
        for u, v in archi:  # u è il nodo da cui parto (l'ho già visto)
            nodiDFS.append(v)
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi


    def buildGraph(self):
        #voglio popolare il grafo con la lista di oggetti (fermate).
        #voglio quindi aggiungere nodi e archi
        #è bene assicurarsi che all'inizio il grafo sia vuoto altrimenti aggiungo nodi a uno esistente
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        #per verifiacare se l'ho costruito bene creo "testModel"
        # tic = datetime.now()
        # self.addedges()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc - tic)
        #
        # tic = datetime.now()
        # self.addedges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc - tic)

        tic = datetime.now()
        self.addedges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc-tic)

    '''SCRIVO 3 METODI DIVERSI PER RIEMPIRE IL GRAFO CHE DIFFRISCONO PER COME ?'''
    def addedges(self ):
        #ciclo su tutte le coppie di nodi e verifico col dao se tra quella coppia c'è una connessione,
        # se c'è aggiungo arco. Se ho un grafo di pochi nodi, ha senso utilizzare questo primo metodo.
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate: #questo doppio ciclo for è un po troppo lungo e fa perdere tempo
                if DAO.hasconn(u, v): #SE ritorna true:
                    self._grafo.add_edge(u, v) #posso aggiungere al grafo la coppia di nodi

    #siccome quesTO addedges1 è lento, penso a un altra soluzione
    def addedges2(self):
        #prendo tutti i nodi connessi a quella fermata e ??
        self._grafo.clear_edges()
        for u in self._fermate:
            for connessione in DAO.getvicini(u): #voglio l'elenco dei vicini del nodo
                v= self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)
                
    '''posso fare ancora meglio di addedges2: posso pensare a un modo di costruire
    gli edge senza fare un ciclo for, ma solo leggendo la tabella connessioni: due nodi sono collegati
    solo se c'è una connessione tra loro, se leggo tutte le connessioni che ho nel dao ho fatto'''
    def addedges3(self): #funzione che mi tira fuori tutti gli archi
        #in questo caso posso aggiungerli tutti in altri casi devo fare dei controlli
        self._grafo.clear_edges()
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